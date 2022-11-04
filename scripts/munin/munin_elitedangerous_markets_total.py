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
    cursor.execute("SELECT `market_type` FROM `markets` GROUP BY `market_type`")
    
    print("graph_title Number of stations known to BirdNet")
    print("graph_category elitedangerous")
    print("graph_vlabel systems")
    
    for row in cursor:
        n = row[0]
        l = n.lower()
        print(f"{l}.label {n}")
        print(f"{l}.min 0")
        print(f"{l}.draw AREASTACK")
        
def output_values():
    cursor = db.cursor()
    cursor.execute("SELECT `market_type`, COUNT(*) FROM `markets` GROUP BY `market_type`")
    
    for row in cursor:
        n = row[0]
        l = n.lower()
        value = row[1]
        print(f"{l}.value {value}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
