#!/usr/bin/env python3

import json
import os
import sys
import time
import mysql.connector

db = mysql.connector.connect(
    host=os.getenv('dbhost'),
    user=os.getenv('dbuser'),
    password=os.getenv('dbpass'),
    database=os.getenv('dbname')
)

def output_config():
    cursor = db.cursor()
    cursor.execute("SELECT `journal_event` FROM `eddn_messages` WHERE `journal_event` IS NOT NULL GROUP BY `journal_event` ")
    
    print("graph_title EDDN journal messages by event type")
    print("graph_category elitedangerous")
    print("graph_vlabel messages/minute")
    print("update_rate " + str(1 * 60))
    for row in cursor:
        n = row[0]
        id = n.lower()
        print(f"{id}.label {n}")
        print(f"{id}.min 0")
        print(f"{id}.draw AREASTACK")
        
def output_values():
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    
    result = {}
    cursor.execute("SELECT `journal_event` FROM `eddn_messages` WHERE `journal_event` IS NOT NULL GROUP BY `journal_event` ")
    for row in cursor:
        id = row[0].lower()
        result[id] = 0
    
    cursor.execute("SELECT `journal_event`, IFNULL(COUNT(`id`), 0) FROM `eddn_messages` WHERE `listener_timestamp` >= %s AND `journal_event` IS NOT NULL GROUP BY `journal_event`", (start_time,))
    
    for row in cursor:
        id = row[0].lower()
        value = row[1]
        result[id] = value
        
    for id in result:
        value = result[id]
        print(f"{id}.value {value}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
        