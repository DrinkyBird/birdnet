import mariadb
import requests
import time
import math
import re
import scrape_config
import subprocess
import os
import sys
from xml.etree import ElementTree
from datetime import datetime

db = mariadb.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

csvs_updated = []
sheets_updated = []

def scrape_goals(language):
    global csvs_updated
    
    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
        'Accept':           'application/json'
    }
    
    response = requests.get("https://api.orerve.net/2.0/website/initiatives/list?lang=" + language, headers=headers)
    print(response.content)
    json = response.json()
    
    active = json['activeInitiatives']
    
    cursor = db.cursor(dictionary=True)
    
    for cg in active:
        id = int(cg['id'])
        title = cg['title']
        expiry = cg['expiry']
        station = cg['market_name']
        system = cg['starsystem_name']
        activity = cg['activityType']
        quantity = int(cg['target_qty'])
        progress = int(cg['qty'])
        commodities = cg['target_commodity_list']
        objective = cg['objective']
        news = cg['news']
        bulletin = cg['bulletin']
        expiry_timestamp = math.floor(time.mktime(datetime.strptime(expiry + ' +0000', "%Y-%m-%d %H:%M:%S %z").timetuple()))
        
        progress_csv = os.path.join(scrape_config.CG_PROGRESS_DIR, f"{id}.csv")
        delta = 0
        
        print(id)
        print(title)
        print(f"{progress}/{quantity}")
        
        now = math.floor(time.time())
        
        sql = f"SELECT `id`, `progress` FROM `goals_{language}` WHERE `id`=%s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row is not None:
            delta = progress - row["progress"]
            sql = f"UPDATE goals_{language} SET expiry=%s, market_name=%s, system_name=%s, activity=%s, quantity=%s, progress=%s, title=%s, commodities=%s, objective=%s, news=%s, bulletin=%s, last_updated=%s WHERE id=%s"
            vals = (expiry_timestamp, station,system, activity, quantity, progress, title, commodities, objective, news, bulletin, now, id)
            cursor.execute(sql, vals)
            print("DUPLICATE!")
        else:
            sql = f"INSERT INTO `goals_{language}` (id, expiry, market_name, system_name, activity, quantity, progress, title, commodities, objective, news, bulletin, last_updated, first_seen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (id, expiry_timestamp, station,system, activity, quantity, progress, title, commodities, objective, news, bulletin, now, now)
            cursor.execute(sql, vals)
            
        db.commit()
            
        if id not in csvs_updated:
            ts = datetime.utcfromtimestamp(now).strftime('%Y-%m-%dT%H:%M:%S')
            csvline = f"{ts}+00:00,{progress},{delta}\n"
            
            if not os.path.isfile(progress_csv):
                with open(progress_csv, "w") as f:
                    f.write("Timestamp,Progress,Delta\n")
                    f.write(csvline)
            else:
                with open(progress_csv, "a") as f:
                    f.write(csvline)
                    
            csvs_updated.append(id)
            
        if id not in sheets_updated:
            subprocess.run([
                "python3", 
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "cg_sheet_update.py"),
                str(id), str(progress), str(delta)
            ])
            sheets_updated.append(id)
        
    
if __name__ == "__main__":
    scrape_goals("en")
    
    if len(sys.argv) >= 2 and sys.argv[1] == "lang":
        scrape_goals("de")
        scrape_goals("fr")
        scrape_goals("es")
        scrape_goals("ru")
