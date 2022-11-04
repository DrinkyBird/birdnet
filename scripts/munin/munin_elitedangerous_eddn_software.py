#!/usr/bin/env python3

import json
import os
import sys
import time
import mysql.connector
import re

db = mysql.connector.connect(
    host=os.getenv('dbhost'),
    user=os.getenv('dbuser'),
    password=os.getenv('dbpass'),
    database=os.getenv('dbname')
)

def filter_id(id):
    id = re.sub('[^0-9a-zA-Z]+', '_', id)
    return id.lower()

def output_config():
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    cursor.execute("SELECT CONCAT(`software_name`, '/', `software_version`) AS `software_full` FROM `eddn_messages` WHERE `listener_timestamp` >= %s GROUP BY `software_full`", (start_time,))
    
    print("graph_args -l 0")
    print("graph_title EDDN messages by software")
    print("graph_category elitedangerous")
    print("graph_vlabel messages/minute")
    print("update_rate " + str(1 * 60))
    for row in cursor:
        n = row[0]
        id = filter_id(n)
        print(f"{id}.label {n}")
        print(f"{id}.min 0")
        
def output_values():
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    cursor.execute("SELECT CONCAT(`software_name`, '/', `software_version`) AS `software_full`, COUNT(*) FROM `eddn_messages` WHERE `listener_timestamp` >= %s GROUP BY `software_full`", (start_time,))
    
    for row in cursor:
        id = filter_id(row[0])
        value = row[1]
        print(f"{id}.value {value}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
        