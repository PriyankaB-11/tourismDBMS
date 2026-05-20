import os
import io
import re
import requests
from PIL import Image
from urllib.parse import urlparse

from config import Config
import mysql.connector

IMG_DIR = os.path.join('static', 'images', 'uploads')
os.makedirs(IMG_DIR, exist_ok=True)

mapping = {
    'Goa Beach Escape': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
    'Goa Beach Escape Deluxe': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
    'Jaipur Heritage Tour': 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80',
    'Jaipur Heritage Walk': 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80',
    'Kerala Backwaters': 'https://picsum.photos/id/1015/1200/800',
    'Kerala Backwaters Relax': 'https://picsum.photos/id/1020/1200/800',
    'Ladakh Adventure': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80',
    'Himalayan Trek': 'https://picsum.photos/id/1018/1200/800',
}

# safe filename helper
def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:120]

# download, resize, save
saved = {}
for name, url in mapping.items():
    try:
        print('Downloading', name)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        image = Image.open(io.BytesIO(resp.content)).convert('RGB')
        # resize & crop to 1200x800 (center-crop)
        target_w, target_h = 1200, 800
        img_w, img_h = image.size
        # compute crop
        aspect_target = target_w / target_h
        aspect_img = img_w / img_h
        if aspect_img > aspect_target:
            # crop width
            new_w = int(aspect_target * img_h)
            offset = (img_w - new_w) // 2
            box = (offset, 0, offset + new_w, img_h)
        else:
            # crop height
            new_h = int(img_w / aspect_target)
            offset = (img_h - new_h) // 2
            box = (0, offset, img_w, offset + new_h)
        cropped = image.crop(box)
        resized = cropped.resize((target_w, target_h), Image.LANCZOS)
        filename = f"{slugify(name)}.jpg"
        out_path = os.path.join(IMG_DIR, filename)
        resized.save(out_path, format='JPEG', quality=85, optimize=True)
        saved[name] = '/'.join(['images', 'uploads', filename])
        print('Saved to', out_path)
    except Exception as e:
        print('Error for', name, e)

# update DB rows to local paths
conn = mysql.connector.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DATABASE, port=Config.MYSQL_PORT)
cur = conn.cursor()
for name, path in saved.items():
    cur.execute('UPDATE destinations SET image_path = %s WHERE name = %s', (path, name))
    print('DB updated:', name, '->', path)
conn.commit()
cur.close()
conn.close()
print('All done, images saved locally and DB updated.')
