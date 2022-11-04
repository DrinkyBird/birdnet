#!/usr/bin/env python3

import json
import os
import sys
import time
import mysql.connector

def output_config():
    print("graph_args -l 0")
    print("graph_title EDDN messages by game type")
    print("graph_category elitedangerous")
    print("graph_vlabel messages/minute")
    print("update_rate " + str(1 * 60))
    
    print("unknown.label Unknown")
    print("unknown.colour AAAAAA")
    print("unknown.min 0")
    print("base.label Elite Dangerous")
    print("base.colour FF6F00")
    print("base.min 0")
    print("horizons.label Elite Dangerous: Horizons")
    print("horizons.colour 0A8BD6")
    print("horizons.min 0")
    print("odyssey.label Elite Dangerous: Odyssey")
    print("odyssey.colour B4956D")
    print("odyssey.min 0")
        
def output_values():
    db = mysql.connector.connect(
        host=os.getenv('dbhost'),
        user=os.getenv('dbuser'),
        password=os.getenv('dbpass'),
        database=os.getenv('dbname')
    )

    start_time = int(time.time() - 60)
    cursor = db.cursor(buffered=False)
    cursor.execute("SELECT `game_type` FROM `eddn_messages` WHERE `listener_timestamp` >= %s", (start_time,))
    
    ed_count = 0
    edo_count = 0
    edh_count = 0
    unk_count = 0
    
    for row in cursor:
        game_type = row[0]
        if game_type == 0:
            ed_count += 1
        elif game_type == 1:
            edh_count += 1
        elif game_type == 2:
            edo_count += 1
        else:
            unk_count += 1

    print(f"unknown.value {unk_count}")
    print(f"base.value {ed_count}")
    print(f"horizons.value {edh_count}")
    print(f"odyssey.value {edo_count}")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "config": 
            output_config()
    else: 
        output_values()
        