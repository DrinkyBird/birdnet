import mariadb
import requests
import time
import math
import re
import scrape_config
import os
from xml.etree import ElementTree
from datetime import datetime
from colorthief import ColorThief


db = mariadb.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

def scrape_store():
    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
        'Accept':           'application/json'
    }
    
    response = requests.get("https://api.zaonce.net/3.0/store/product", headers=headers)
    json = response.json()
    
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("UPDATE `store` SET `available` = 0")
    
    for item in json:
        sku = item['sku']
        title = item['title']
        current_price = item['current_price']
        original_price = item['original_price']
        extra_type = item['extra_type']
        extra_subtype = item['extras_subtype']
        slug = item['url_key']
        available = item['available']
        thumbnail = item['thumbnail']
        image = item['image']
        small_image = item['small_image']
        description = item['description']
        short_description = item['short_description']
        minimum_client_version = item['minimum_client_version']
        minimum_season = item['minimum_season']
        attributes = item['attribute_list']
        colour = None
        
        now = math.floor(time.time())
        
        sql = "SELECT COUNT(*) FROM `store` WHERE `sku` = %s"
        vals = (sku,)
        cursor.execute(sql, vals)
        if cursor.fetchone()["COUNT(*)"] == 1:
            sql = """
                UPDATE `store` SET
                    `title` = %s,
                    `current_price` = %s,
                    `original_price` = %s,
                    `type` = %s,
                    `subtype` = %s,
                    `slug` = %s,
                    `available` = %s,
                    `thumbnail` = %s,
                    `image` = %s,
                    `small_image` = %s,
                    `description` = %s,
                    `short_description` = %s,
                    `minimum_client_version` = %s,
                    `minimum_season` = %s,
                    `last_updated` = %s
                WHERE `sku` = %s
            """
            vals = (title, current_price, original_price, extra_type, extra_subtype, slug, available, thumbnail, image, small_image, description, short_description, minimum_client_version, minimum_season, now, sku)
            cursor.execute(sql, vals)
        else:
            try:
                resp = requests.get("https://dlc.elitedangerous.com/images/med/" + image, headers=headers, stream=True)
                thief = ColorThief(resp.raw)
                r, g, b = thief.get_color()
                colour = f"{r:02x}{g:02x}{b:02x}"
            except Exception as e:
                traceback.print_exc()
                pass
            
            sql = """
                INSERT INTO `store`
                    (`sku`, `title`, `current_price`, `original_price`, `type`, `subtype`, `slug`, `available`, `thumbnail`, `image`, `small_image`, `description`, `short_description`, `minimum_client_version`, `minimum_season`, `first_seen`, `last_updated`, `colour`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            vals = (sku, title, current_price, original_price, extra_type, extra_subtype, slug, available, thumbnail, image, small_image, description, short_description, minimum_client_version, minimum_season, now, now, colour)
            cursor.execute(sql, vals)
        
        for attr in attributes:
            sql = "INSERT IGNORE INTO `store_attributes` (`sku`, `attribute`) VALUES (%s, %s)"
            vals = (sku, attr)
            cursor.execute(sql, vals)
    
    db.commit()

if __name__ == "__main__":
    scrape_store()
