import mysql.connector
import time
import math
import re
import subprocess
import os
import scrape_config
import json_stream
import sys
import ciso8601
import time
import datetime

db = mysql.connector.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

if __name__ == "__main__":
    json_path = sys.argv[1]
    i = 0
    with open(json_path, "r") as f:
        data = json_stream.load(f)
        
        cursor = db.cursor()
        
        for system in data:
            id = system["id64"]
            name = system["name"]
            coords = system["coords"]
            x = coords["x"]
            y = coords["y"]
            z = coords["z"]
            date_str = system["date"]
            timestamp = int(ciso8601.parse_datetime(date_str).replace(tzinfo=datetime.timezone.utc).timestamp())
                
            if timestamp != 0:
                cursor.execute(
                    "INSERT IGNORE INTO `systems` (`id`, `name`, `x`, `y`, `z`, `last_updated`) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id, name, x, y, z, timestamp)
                )
            
            i += 1
            
            if i % 10000 == 0:
                print(f"{i:,}")
                db.commit()
                cursor = db.cursor()
            
        db.commit()
        print(f"total = {i}")