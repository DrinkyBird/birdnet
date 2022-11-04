import mysql.connector
import requests
import time
import math
from bs4 import BeautifulSoup
from datetime import datetime

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

db = mysql.connector.connect(
    host="localhost",
    user="galnet",
    password="lrPgsyE26nZr4jwI",
    database="galnet"
)

def scrape_page(page_url, language):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    cursor = db.cursor()
    
    articles = soup.find_all("div", class_="article")
    i = 0
    for article in articles:
        publication_date = article.find_all("p", class_="small")[0].text.strip()
        title = article.find_all("h3", class_="galnetNewsArticleTitle")[0].text.strip()
        text = article.find_all("p", class_="")[0].text.strip()
        link = article.find_all("a", class_="")[0]['href']
        
        link_parts = link.split('/')
        guid = link_parts[len(link_parts) - 1]
        
        date_day = int(publication_date.split(' ')[0])
        date_month = MONTHS.index(publication_date.split(' ')[1]) + 1
        date_year = int(publication_date.split(' ')[2]) - 1286
        
        dt = datetime(date_year, date_month, date_day, 0, 0, 0)
        timestamp = math.floor(time.mktime(dt.timetuple()))
        timestamp += len(articles) - i - 1
        
        if not title:
            lines = text.split('\n')
            title = lines.pop(0)
            text = '\n'.join(lines)
            
        text = text.replace('<br />', '')
        
        sql = "SELECT COUNT(*) FROM `posts_"+language+"` WHERE `guid`=%s"
        cursor.execute(sql, (guid,))
        if cursor.fetchone()[0] != 0:
            print("DUPLICATE!")
            continue
        
        sql = "INSERT INTO `posts_"+language+"` (guid, title, text, date, appeared) VALUES (%s, %s, %s, %s, %s)"
        vals = (guid, title, text, timestamp, time.time())
        cursor.execute(sql, vals)
        
        i += 1
        
    db.commit()
        
def scrape_html(page_url, language):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    days = soup.find_all("a", class_="galnetLinkBoxLink")
    for day in days:
        link = day['href']
        url = page_url + link
        print(url)
        
        scrape_page(url, language)
    
if __name__ == "__main__":
    scrape_html("https://community.elitedangerous.com/en", "en")
    scrape_html("https://community.elitedangerous.com/de", "de")
    scrape_html("https://community.elitedangerous.com/fr", "fr")