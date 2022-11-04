import mysql.connector
import requests
import time
import math
import re
from xml.etree import ElementTree
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="galnet",
    password="lrPgsyE26nZr4jwI",
    database="galnet"
)

def scrape_rss(feed_url, language):
    response = requests.get(feed_url)
    tree = ElementTree.fromstring(response.content)
    #root = tree.getroot()
    
    cursor = db.cursor()
    
    for item in tree.findall('.//item'):
        guid = item.find('guid').text
        title = item.find('title').text
        description = item.find('description').text.replace('<br />', '')
        pubDate = item.find('pubDate').text
        timestamp = math.floor(time.mktime(datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z").timetuple()))
        print(guid)
        print(title)
        print(description)
        print(pubDate)
        print(timestamp)
        
        sql = "SELECT COUNT(*) FROM `posts_"+language+"` WHERE `guid`=%s"
        cursor.execute(sql, (guid,))
        if cursor.fetchone()[0] != 0:
            print("DUPLICATE!")
            continue
        
        sql = "INSERT INTO `posts_"+language+"` (guid, title, text, date, appeared) VALUES (%s, %s, %s, %s, %s)"
        vals = (guid, title, description, timestamp, time.time())
        cursor.execute(sql, vals)
        
    db.commit()
    
if __name__ == "__main__":
    scrape_rss("https://community.elitedangerous.com/en/galnet-rss", "en")
    scrape_rss("https://community.elitedangerous.com/de/galnet-rss", "de")
    scrape_rss("https://community.elitedangerous.com/fr/galnet-rss", "fr")