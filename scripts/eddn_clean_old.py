import mysql.connector
import requests
import time
import math
import re
import scrape_config
from xml.etree import ElementTree
from datetime import datetime

db = mysql.connector.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

if __name__ == "__main__":
    ts = int(time.time() - 86400)
    cur = db.cursor()
    
    total = 0
    while True:
        sql = "DELETE FROM `eddn_messages` WHERE `listener_timestamp` < %s ORDER BY `id` ASC LIMIT 100000"
        cur.execute(sql, (ts,))
        
        affected = cur.rowcount
        total += affected
        
        if affected < 1:
            break
        else:
            print(f"Deleted {affected:,} rows")
            
    cur.execute("OPTIMIZE TABLE `eddn_messages`")
    
    total = 0
    while True:
        sql = "DELETE FROM `docked_messages` WHERE `timestamp` < %s ORDER BY `id` ASC LIMIT 100000"
        cur.execute(sql, (ts,))
        
        affected = cur.rowcount
        total += affected
        
        if affected < 1:
            break
        else:
            print(f"Deleted {affected:,} rows")
            
    cur.execute("OPTIMIZE TABLE `docked_messages`")
            
    print(f"Total: {total:,} rows")
