import mysql.connector
from config import Config

more = [
    dict(name='Ladakh Adventure', location='Ladakh, India', description='High-altitude lakes, monasteries, and vast landscapes.', price=19999.00, image='images/uploads/ladakh.svg', available_slots=8),
    dict(name='Himalayan Trek', location='Himachal/Uttrakhand, India', description='Multi-day treks across alpine meadows and mountain passes.', price=15999.00, image='images/uploads/himalayas.svg', available_slots=20),
    dict(name='Goa Beach Escape Deluxe', location='Goa, India', description='Luxury beach stay with water sports and nightlife.', price=24999.00, image='images/uploads/goa.svg', available_slots=15),
    dict(name='Jaipur Heritage Walk', location='Jaipur, India', description='Guided exploration of forts and palaces with cultural shows.', price=8999.00, image='images/uploads/jaipur.svg', available_slots=22),
    dict(name='Kerala Backwaters Relax', location='Alleppey, India', description='Calm houseboat journeys with local cuisine.', price=13999.00, image='images/uploads/kerala.svg', available_slots=12),
]

conn = mysql.connector.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DATABASE, port=Config.MYSQL_PORT)
cur = conn.cursor()
for d in more:
    cur.execute("SELECT id FROM destinations WHERE name = %s", (d['name'],))
    if cur.fetchone():
        print('Exists:', d['name'])
        continue
    cur.execute(
        "INSERT INTO destinations (name, location, description, price, image_path, available_slots) VALUES (%s,%s,%s,%s,%s,%s)",
        (d['name'], d['location'], d['description'], d['price'], d['image'], d['available_slots'])
    )
    print('Inserted:', d['name'])
conn.commit()
cur.close()
conn.close()
print('Done')

# --- also set remote image URLs for nicer photos ---
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
    if cur.rowcount:
        print('Updated image for:', name)
    else:
        print('No row found to update for:', name)
conn.commit()
cur.close()
conn.close()
print('Image updates done')
