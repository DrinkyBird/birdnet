import mysql.connector
import math
import scrape_config
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

IMAGE_SIZE = 2 * 1024
GALRADIUS = 45000
GALDIAMETER = GALRADIUS * 2
FONT_SIZE = int(20 * (IMAGE_SIZE / 1024))

heatmap_image = Image.new('RGBA', (IMAGE_SIZE, IMAGE_SIZE))
galaxy_image = Image.open('resources/img_ed_galaxy.jpg', 'r')
galaxy_image = galaxy_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.BILINEAR)
final_image = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
draw = ImageDraw.Draw(final_image)
font = ImageFont.truetype("resources/PTMono-Regular.ttf", FONT_SIZE)

SAGA_X = 25.2188
SAGA_Z = 25900.0

db = mysql.connector.connect(
    host=scrape_config.DB_HOST,
    user=scrape_config.DB_USER,
    password=scrape_config.DB_PASSWORD,
    database=scrape_config.DB_NAME
)

def scale_galaxy_coords(x, z):
    x = x - SAGA_X
    z = z - SAGA_Z
    sx = int(((x + GALRADIUS) / GALDIAMETER) * IMAGE_SIZE)
    sz = int(((z + GALRADIUS) / GALDIAMETER) * IMAGE_SIZE)
        
    return (sx, IMAGE_SIZE - sz)

if __name__ == "__main__":
    cursor = db.cursor(dictionary=True, buffered=False)
    total_systems = 0

    sql = "SELECT `x`, `y`, `z` FROM `systems`"
    cursor.execute(sql)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
            
        total_systems += 1
            
        x = row['x']
        y = row['y']
        z = row['z']
        
        sx, sz = scale_galaxy_coords(x, z)
        
        pixelpos = (sx, sz)
        
        r, g, b, a = heatmap_image.getpixel(pixelpos)
        if r >= 255 and g >= 255 and b >= 255:
            continue
        
        pr = 0
        pg = 255
        pb = 0
        
        if y > 0:
            pr = int(max(0, min(255, (y / 500.0) * 255.0)))
        elif y < 0:
            pb = int(max(0, min(255, (-y / 500.0) * 255.0)))
            
        val = min(255, a + 24)
        
        heatmap_image.putpixel(pixelpos, (r + pr, g + pg, b + pb, val))
        
    final_image.paste(galaxy_image)
    final_image.paste(heatmap_image, (0,0), heatmap_image)
        
    draw.text((0, FONT_SIZE * 0), "All systems map", font=font)
    draw.text((0, FONT_SIZE * 1), f"{total_systems:,} systems", font=font)
    draw.text((0, FONT_SIZE * 2), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), font=font)
    draw.text((0, FONT_SIZE * 3), "elite.drinkybird.net", font=font)

    final_image.save("galaxy.png")