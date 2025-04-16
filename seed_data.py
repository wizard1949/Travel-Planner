from app import app
from models import db, Destination

# Sample data
destinations = [
    Destination(name='Paris', country='France', cost=30000, duration=5, image_url='https://dynamic-media-cdn.tripadvisor.com/media/photo-o/17/15/6d/d6/paris.jpg?w=400&h=300&s=1'),
    Destination(name='Bali', country='Indonesia', cost=15000, duration=7, image_url='https://media.digitalnomads.world/wp-content/uploads/2021/01/20120709/bali-for-digital-nomads.jpg'),
    Destination(name='Switzerland', country='Switzerland', cost=40000, duration=10, image_url='https://cdn.britannica.com/65/162465-050-9CDA9BC9/Alps-Switzerland.jpg'),
    Destination(name='Rome', country='Italy', cost=35000, duration=6, image_url='https://www.volunteerforever.com/wp-content/uploads/2024/05/dan-novac-1naE8177_bI-unsplash-e1716212753925.jpg'),
    Destination(name='Maui', country='USA', cost=50000, duration=8, image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHRGnj7Xf1X6KWD9SzimBWpwrnSIkCDj74BD7cBJRmi26MVoeF2KCUQxQdyJ9PkCdwYAs&usqp=CAU'),
    Destination(name='Tokyo', country='Japan', cost=45000, duration=9, image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8G32ugANPRtjhHv2qCceXdaM55xg0eS4LAw&s'),
]

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.bulk_save_objects(destinations)
    db.session.commit()
    print("✅ Sample destinations added.")
