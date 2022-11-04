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
    print("graph_title Number of systems known to BirdNet")
    print("graph_category elitedangerous")
    print("graph_vlabel systems")
    print("count.label systems")
    print("count.min 0")
    print("count.draw AREA")
        
def output_values():
    start_time = int(time.time() - 60)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM `systems`")
    row = cursor.fetchone()
    
    if row is not None:
        value = row[0]
        print(f"count.value {value}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
        
