# generate_users.py
import random
import string
from faker import Faker
from db import db
from models.utilizatori import Utilizator
from main import app

fake = Faker()

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def generate_user(index):
    email = f"user{index}@example.com"
    parola = generate_random_password()
    rol = random.randint(1, 3)  # assuming there are 3 roles
    nume = fake.last_name()
    prenume = fake.first_name()
    serieActIdentitate = ''.join(random.choices(string.ascii_uppercase, k=2))
    numarActIdentate = ''.join(random.choices(string.digits, k=6))
    reseteazaParola = random.choice([True, False])
    
    return Utilizator(
        email=email,
        parola=parola,
        rol=rol,
        nume=nume,
        prenume=prenume,
        serieActIdentitate=serieActIdentitate,
        numarActIdentate=numarActIdentate,
        reseteazaParola=reseteazaParola
    )

with app.app_context():
    for i in range(1, 101):
        user = generate_user(i)
        db.session.add(user)
    db.session.commit()

print("100 users have been generated and added to the database.")
