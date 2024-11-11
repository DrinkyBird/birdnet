import mariadb
import requests
import sys
import scrape_config
from datetime import datetime

db = mariadb.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

if __name__ == "__main__":
    news_id = sys.argv[1]
    news_lang = sys.argv[2]

    if news_lang not in scrape_config.DISCORD_WEBHOOKS_NEWS:
        print(f"{news_lang} has no news webhook")
        sys.exit(0)

    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM `posts_{news_lang}` WHERE `guid`=%s", (news_id,))
    row = cursor.fetchone()

    headers = {
        'User-Agent':       scrape_config.USER_AGENT,
    }

    body = ""
    lines = row["text"].split("\n")
    for i in range(len(lines)):
        body += "> " + lines[i] + "\n"
        if i < len(lines) - 1:
            body += "> \n"
    if len(body) > 2000:
        body = body[:1400] + "..."

    image = None
    if row["image"]:
        image = f"https://hosting.zaonce.net/elite-dangerous/galnet/{row['image']}.png"

    birdnet_url = f"{scrape_config.SITE_URL}/?guid={row['guid']}"
    edcom_url = f"https://www.elitedangerous.com/news/galnet/{row['slug']}"
    olded_url = f"https://community.elitedangerous.com/galnet/uid/{row['guid']}"
    content = ""
    content += f"# [{row['title']}](<{birdnet_url}>)\n\n"
    content += body + "\n"
    content += f"-# View on: [BirdNet](<{birdnet_url}>), [elitedangerous.com](<{edcom_url}>), or [community.elitedangerous.com](<{olded_url}>). "
    if image is not None:
        content += f"[Article image]({image})"

    params = {
        "username": "Galnet News",
        "allowed_mentions": { "parse": [] },
        "content": content
    }

    print(params)
    r = requests.post(scrape_config.DISCORD_WEBHOOKS_NEWS[news_lang], headers=headers, json=params)
    print(r)
    print(r.text)
