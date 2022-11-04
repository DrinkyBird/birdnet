#!/usr/bin/env python3

import json
import os
import sys
import time
import mysql.connector
import zlib

db = mysql.connector.connect(
    host=os.getenv('dbhost'),
    user=os.getenv('dbuser'),
    password=os.getenv('dbpass'),
    database=os.getenv('dbname')
)

def output_config():
    print("graph_title EDDN unique user count")
    print("graph_category elitedangerous")
    print("graph_vlabel users")
    print("users.label Users")
    print("users.min 0")
    print("update_rate " + str(1 * 60))
        
def output_values():
    star_types = []
    planet_types = []
    
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM ( SELECT COUNT(*) FROM `eddn_messages`  WHERE `listener_timestamp` >= %s GROUP BY `uploader_id` ) t", (start_time,))
    
    value = cursor.fetchone()[0]
    print(f"users.value {value}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()