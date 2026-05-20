import mysql.connector
from config import Config

conn = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE,
    port=Config.MYSQL_PORT,
)
cur = conn.cursor()
cur.execute("SELECT id, image_path FROM destinations")
rows = cur.fetchall()
updated = 0
for row_id, image_path in rows:
    if image_path and "\\" in image_path:
        fixed = image_path.replace("\\", "/")
        cur.execute("UPDATE destinations SET image_path = %s WHERE id = %s", (fixed, row_id))
        updated += 1
conn.commit()
print('rows updated:', updated)
cur.close()
conn.close()
