import os
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import IoC, Feeds, Alerts, Users

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

fake = Faker(["en_US"])

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


for x in range(100):
    new_user = IoC(
        type = fake.random_element(["IP", "Domain", "Hash"]),
        value = fake.ipv4(),
        source = fake.url(),
        severity = fake.random_element(["Low", "Medium", "High", "Critical"]),
        timestamp = fake.date_time()
    )
    session.add(new_user)

    session.commit()
print("Successfully inserted fake data")
session.close()