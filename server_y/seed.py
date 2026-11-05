# seed.py
# resoruce: https://neon.com/docs/guides/sqlalchemy-migrations

from database import SessionLocal
from models import ReactionsY

def seed_data():
    db =  SessionLocal()

    reactions_y = [
        ReactionsY(post_id=1, account_id="997fe2db-1b71-4f7f-ba95-ba95b6034982", reaction_text="hate" )
    ]
    db.add_all(reactions_y)
    db.commit()

    print("Data seeded successfully.")

if __name__ == "__main__":
    seed_data()
