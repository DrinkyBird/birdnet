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

def fix_offset(st):
    i = st.rfind(':')
    return st[:i] + st[i + 1:]

def scrape_webapi(apilang, dblang):
    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
        'Accept':           'application/json'
    }
    
    cursor = db.cursor()
    i = 0
    
    url = "https://cms.zaonce.net/"+apilang+"/jsonapi/node/galnet_article?sort=-published_at&page[offset]=0&page[limit]=50"
    print(url)
    r = requests.get(url, headers=headers)
    response = r.json()
    
    for article in response['data']:
        if article['type'] != 'node--galnet_article':
            continue
            
        attribs = article['attributes']
        title = attribs['title']
        guid = attribs['field_galnet_guid']
        text = attribs['body']['value'].replace('\r', '')
        pubDate = fix_offset(attribs['published_at'])
        timestamp = math.floor(time.mktime(datetime.strptime(pubDate, "%Y-%m-%dT%H:%M:%S%z").timetuple()))
        image = attribs['field_galnet_image']
        slug = attribs['field_slug']
        
        print(slug)
        
        sql = "SELECT COUNT(*) FROM `posts_"+dblang+"` WHERE `guid`=%s"
        cursor.execute(sql, (guid,))
        if cursor.fetchone()[0] != 0:
            print("DUPLICATE!")
            sql = "UPDATE `posts_"+dblang+"` SET title=%s, text=%s, date=%s, appeared=%s, image=%s, slug=%s WHERE guid=%s"
            vals = (title, text, timestamp, time.time(), image, slug, guid)
            cursor.execute(sql, vals)
        else:
            sql = "INSERT INTO `posts_"+dblang+"` (guid, title, text, date, appeared, image, slug) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            vals = (guid, title, text, timestamp, time.time(), image, slug)
            cursor.execute(sql, vals)
        
    db.commit()

if __name__ == "__main__":
    scrape_webapi("en-GB", "en")
    scrape_webapi("de-DE", "de")
    scrape_webapi("fr-FR", "fr")
    scrape_webapi("ru-RU", "ru")
    scrape_webapi("es-ES", "es")