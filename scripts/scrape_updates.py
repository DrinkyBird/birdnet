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

#https://cms.zaonce.net/en-GB/jsonapi/node/game_update?include=field_image_entity.field_media_image,field_game_singular&filter[field_game_singular.field_slug]=elite-dangerous&sort[sort-created][path]=created&sort[sort-created][direction]=DESC&page[offset]=0&page[limit]=6

def fix_offset(st):
    i = st.rfind(':')
    return st[:i] + st[i + 1:]

def scrape_webapi():
    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
        'Accept':           'application/json'
    }
    
    params = {
        "filter[field_game_singular.field_slug]": "elite-dangerous",
        "sort": "-published_at",
        "page[limit]": 50
    }
    
    cursor = db.cursor()
    i = 0
    
    url = "https://cms.zaonce.net/en-GB/jsonapi/node/game_update"
    print(url)
    r = requests.get(url, headers=headers, params=params)
    response = r.json()
    
    for article in response['data']:
        if article['type'] != 'node--game_update':
            continue
            
        attribs = article['attributes']
        title = attribs['title']
        text = attribs['body']['value'].replace('\r', '')
        notes = attribs['field_patch_notes']['value'].replace('\r', '')
        pubDate = fix_offset(attribs['published_at'])
        timestamp = math.floor(time.mktime(datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%S%z").timetuple()))
        version = attribs['field_version']['value']
        
        sql = """
            INSERT INTO `updates`
                (`version`, `title`, `text`, `notes`, `date`)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                `title` = %s,
                `text` = %s,
                `notes` = %s,
                `date` = %s
        """
        vals = (
            version, title, text, notes, timestamp,
            title, text, notes, timestamp
        )
        
        cursor.execute(sql, vals)
        
    db.commit()

if __name__ == "__main__":
    scrape_webapi()
