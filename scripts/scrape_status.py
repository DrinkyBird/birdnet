import requests
import json
import mariadb
import math
import time
import scrape_config
from datetime import datetime

db = mariadb.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

def scrape_status():
    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
        'Accept':           'application/json'
    }
    
    cursor = db.cursor(dictionary=True)
    
    url = "https://hosting.zaonce.net/launcher-status/status.json"
    print(url)
    r = requests.get(url, headers=headers)
    response = r.json()
    
    status_text = response["text"]
    status_code = response["status"]
    
    cursor.execute("SELECT * FROM `status` ORDER BY `timestamp` DESC LIMIT 1")
    previous = cursor.fetchone()
    
    now = math.floor(time.time())
    
    if previous is None:
        cursor.execute("INSERT INTO status (timestamp, status_code, status_text) VALUES (%s, %s, %s)", (now, status_code, status_text))
    else:
        previous_text = previous["status_text"]
        previous_code = previous["status_code"]
        
        if status_text != previous_text or status_code != previous_code:
            cursor.execute("INSERT INTO status (timestamp, status_code, status_text) VALUES (%s, %s, %s)", (now, status_code, status_text))
        
    db.commit()

if __name__ == "__main__":
    scrape_status()