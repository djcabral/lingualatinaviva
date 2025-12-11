import sys
import os
from sqlmodel import SQLModel, select
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import engine, get_session
from database import SystemSetting

def create_settings_table():
    print("Creating SystemSetting table...")
    SQLModel.metadata.create_all(engine)
    print("SystemSetting table created successfully.")

def seed_settings():
    print("Seeding default settings...")
    with get_session() as session:
        # Check if email setting exists
        setting = session.get(SystemSetting, "contact_email")
        if not setting:
            print("Seeding contact_email...")
            setting = SystemSetting(
                key="contact_email",
                value="lengualatinaviva@gmail.com",
                description="Correo electrónico de contacto mostrado en el pie de página",
                updated_at=datetime.utcnow()
            )
            session.add(setting)
            session.commit()
            print("contact_email seeded.")
        else:
            print("contact_email already exists.")

if __name__ == "__main__":
    create_settings_table()
    seed_settings()
