#!/usr/bin/env python3

from app import app
from models import db, Gift
from faker import Faker
from random import randint

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Gift.query.delete()
        
        # gifts = []
        
        for _ in range(0,6):
            # gift = Gift(name=faker.name(), price=(randint(1,1000)/100.0))
            gift = Gift(name=faker.commerce.product(), price=faker.commerce.price())
            # gifts.append(gift)
            db.session.add(gift)
            
        db.session.commit()

        print("Seeding complete!")
