import time
import time
import math
import mysql.connector
import scrape_config
from datetime import datetime

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

db = mysql.connector.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

if __name__ == "__main__":
    cursor = db.cursor()
    
    now = math.floor(time.time())
    start_time = now - (2 * DAY)
    start_time = start_time - (start_time % HOUR)
    end_time = now - (now % HOUR)
    update_period = HOUR
    
    print(f"Now = {now}")
    print(f"start_time = {start_time}")
    
    data = []
    
    current = start_time
    while current < end_time:
        end_period = min(now, current + update_period)
        sql = "SELECT COUNT(*) FROM eddn WHERE gateway_timestamp >= %s AND gateway_timestamp < %s"
        vals = (current, end_period)
        cursor.execute(sql, vals)
        
        value = cursor.fetchone()[0]
        if now <= end_time or end_period >= end_time:
            break
        
        data.append((current, end_period, value))
        
        current += update_period
        
    while data[0][2] == 0:
        data.pop(0)
        
    cursor = db.cursor(buffered=True)
    cursor.execute("TRUNCATE TABLE eddn_activity_graph")
    for start_period, end_period, value in data:
        print(start_period)
        print(end_period)
        print(value)
        
        sql = "INSERT INTO `eddn_activity_graph` (start_period, end_period, value) VALUES (%s, %s, %s)"
        vals = (start_period, end_period, value)
        cursor.execute(sql, vals)
        
    cursor.execute("OPTIMIZE TABLE eddn_activity_graph")
        
    db.commit()