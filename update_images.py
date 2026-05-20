import mysql.connector
from config import Config

mapping = {
    'Goa Beach Escape': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
    'Goa Beach Escape Deluxe': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
    'Jaipur Heritage Tour': 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80',
    'Jaipur Heritage Walk': 'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80',
    'Kerala Backwaters': 'https://images.unsplash.com/photo-1505765053452-4a3f86a0c3c8?auto=format&fit=crop&w=1200&q=80',
    'Kerala Backwaters Relax': 'https://images.unsplash.com/photo-1505765053452-4a3f86a0c3c8?auto=format&fit=crop&w=1200&q=80',
    'Ladakh Adventure': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80',
    'Himalayan Trek': 'https://images.unsplash.com/photo-1508264165352-258a6a4d7c4a?auto=format&fit=crop&w=1200&q=80',
}

conn = mysql.connector.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DATABASE, port=Config.MYSQL_PORT)
cur = conn.cursor()
for name, url in mapping.items():
    cur.execute("UPDATE destinations SET image_path = %s WHERE name = %s", (url, name))
    print('Updated:', name)
conn.commit()
cur.close()
conn.close()
print('Done')
