import time
import zmq
import zlib
import json
import time
import math
import mysql.connector
import scrape_config
import requests
import urllib.parse
import datetime
import traceback
import ciso8601
import re

CLIENT_TYPE_UNKNOWN = None
CLIENT_TYPE_ED = 0
CLIENT_TYPE_EDH = 1
CLIENT_TYPE_EDO = 2

SYSTEM_FIELDS = {
    "SystemAddress":        "id",
    "StarSystem":           "name",
}

MARKET_FIELDS = {
    "MarketID":                             "id",
    "SystemAddress":                        "system_id",
    "StationName":                          "name",
    "StationType":                          "market_type",
    "DistFromStarLS":                       "arrival_distance",
}

db = None

EDDN_RELAY = "tcp://eddn.edcd.io:9500"
EDDN_TIMEOUT = 600000

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.setsockopt(zmq.RCVTIMEO, EDDN_TIMEOUT)
    
def update_system(data):
    now = math.floor(time.time())
    message = data['message']
    if 'SystemAddress' not in message:
        return

    system_id = message['SystemAddress']
    
    fields = {
        'last_updated': now
    }
    
    for key in message:
        value = message[key]
        if key in SYSTEM_FIELDS:
            fields[SYSTEM_FIELDS[key]] = value
            
    if 'StarPos' in message:
        fields['x'] = message['StarPos'][0]
        fields['y'] = message['StarPos'][1]
        fields['z'] = message['StarPos'][2]
        
    cursor = db.cursor()
            
    field_names = []
    field_values = []
    fields_sets = []
    query_vals = []
    
    for key in fields:
        field_names.append(key)
        field_values.append("%s")
        query_vals.append(fields[key])
        
    for key in fields:
        if key == 'id' or key == 'first_appeared':
            continue
        fields_sets.append(f"`{key}`=%s")
        query_vals.append(fields[key])
        
    sql = f"INSERT INTO `systems` ({', '.join(field_names)}) VALUES ({', '.join(field_values)}) ON DUPLICATE KEY UPDATE {', '.join(fields_sets)}"
    cursor.execute(sql, query_vals)
    db.commit()
        
def update_market(data):
    now = math.floor(time.time())
    message = data['message']
    if 'MarketID' not in message:
        return
        
    cursor = db.cursor()
        
    station_id = message['MarketID']
    
    fields = {
        'last_updated': now,
        'first_appeared': now,
    }
        
    for key in message:
        value = message[key]
        if key in MARKET_FIELDS:
            fields[MARKET_FIELDS[key]] = value
            
    field_names = []
    field_values = []
    fields_sets = []
    query_vals = []
    
    for key in fields:
        field_names.append(key)
        field_values.append("%s")
        query_vals.append(fields[key])
        
    for key in fields:
        if key == 'id' or key == 'first_appeared':
            continue
        fields_sets.append(f"`{key}`=%s")
        query_vals.append(fields[key])
        
    sql = f"INSERT INTO `markets` ({', '.join(field_names)}) VALUES ({', '.join(field_values)}) ON DUPLICATE KEY UPDATE {', '.join(fields_sets)}"
    cursor.execute(sql, query_vals)
    db.commit()
    
def insert_message(data):
    message = data['message']
    header = data['header']
    schemaRef = data['$schemaRef']
    gateway_timestamp = int(ciso8601.parse_datetime(header['gatewayTimestamp']).replace(tzinfo=datetime.timezone.utc).timestamp())
                
    game_type = CLIENT_TYPE_UNKNOWN
    if 'odyssey' in message and message['odyssey']:
        game_type = CLIENT_TYPE_EDO
    elif 'horizons' in message:
        if message['horizons']:
            game_type = CLIENT_TYPE_EDH
        else:
            game_type = CLIENT_TYPE_ED
        
    journal_type = None
    if schemaRef == 'https://eddn.edcd.io/schemas/journal/1':
        journal_type = message["event"]
        
    sql = f"INSERT INTO `eddn_messages` (uploader_id, software_name, software_version, gateway_timestamp, listener_timestamp, game_type, schema_ref, journal_event) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    query_vals = (header["uploaderID"], header["softwareName"], header["softwareVersion"], gateway_timestamp, int(time.time()), game_type, schemaRef, journal_type)
    cursor.execute(sql, query_vals)
    db.commit()
    
def insert_docked(data):
    update_system(data)
    update_market(data)
    
    if "message" in data:
        message = data["message"]
        if "SystemAddress" in message and "MarketID" in message:
            cursor = db.cursor()
            sql = "INSERT INTO `docked_messages` (`timestamp`, `system_id`, `market_id`) VALUES (%s, %s, %s)"
            values = (int(time.time()), message["SystemAddress"], message["MarketID"])
            cursor.execute(sql, values)
            db.commit()
            
def handle_fsssignaldiscovered(data):
    if "message" in data:
        message = data["message"]
        cursor = db.cursor()
        if "signals" in message and "SystemAddress" in message:
            for signal in message["signals"]:
                if "IsStation" in signal and signal["IsStation"] == True:
                    signal_name = signal["SignalName"]
                    
                    xpr = "^(.*) ([A-Z0-9][A-Z0-9][A-Z0-9]\-[A-Z0-9][A-Z0-9][A-Z0-9])$"
                    matches = re.findall(xpr, signal_name)
                    if len(matches) == 1 and len(matches[0]) == 2:
                        name = matches[0][0]
                        callsign = matches[0][1]
                        now = int(time.time())
                        
                        sql = "INSERT INTO `carrier_names` (`callsign`, `name`, `last_updated`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `name` = %s, `last_updated` = %s"
                        values = (callsign, name, now, name, now)
                        cursor.execute(sql, values)
        db.commit()
    
if __name__ == "__main__":
    while True:
        db = mysql.connector.connect(
            host=scrape_config.DB_HOST,
            user=scrape_config.DB_USER,
            password=scrape_config.DB_PASSWORD,
            database=scrape_config.DB_NAME
        )
        socket.connect(EDDN_RELAY)
        print("Ready")
        
        while True:
            try:
                cursor = db.cursor()
                message = socket.recv()
                
                if message == False:
                    socket.disconnect(EDDN_RELAY)
                    break
                    
                message = zlib.decompress(message)
                data = json.loads(message)
                
                if '$schemaRef' not in data:
                    continue
                
                message = data['message']
                header = data['header']
                schemaRef = data['$schemaRef']
                
                insert_message(data)
                        
                if schemaRef == 'https://eddn.edcd.io/schemas/journal/1':
                    eventType = message['event']
                    if eventType in ['FSDJump', 'Location', 'Docked', 'Scan', 'CarrierJump']:
                        update_system(data)
                        update_market(data)
                    if eventType in ["Docked", "Location"]:
                        insert_docked(data)
                        
                if schemaRef == 'https://eddn.edcd.io/schemas/fsssignaldiscovered/1':
                    handle_fsssignaldiscovered(data)
                        
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(5)
                break

