from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'sqlite:///bot_database.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Default user columns 
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True, nullable=True)
    phone_number = Column(String, nullable=True)
    first_start_date = Column(DateTime, default=datetime.utcnow)
    source_start = Column(String, nullable=True)
    is_admin_session_active = Column(Boolean, default=False)

    # To subscribe channels json
    subscribed_channels = Column(JSON, default=[])

    # Access channels
    subscribed_hmelnytskyi = Column(Boolean, default=False)
    subscribed_lutsk = Column(Boolean, default=False)
    subscribed_kiev = Column(Boolean, default=False)
    subscribed_ternopil = Column(Boolean, default=False)

    # If user subscribed to all access channels
    subscribed_all = Column(Boolean, default=False)

    def update_subscribed_all(self):
        self.subscribed_all = all(getattr(self, f"subscribed_{channel_name}") for channel_name in ["hmelnytskyi", "lutsk", "kiev", "ternopil"])

class ToSubscripeChannel(Base):
    __tablename__ = 'to_subscribe_channels'

    name = Column(String, unique=True, index=True)
    link = Column(String)

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    link = Column(String)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Дефолтные записи перед созданием таблиц
default_channels = [
    {"id": 1949156593, "name": 'Хмельницкий', "link": 'https://t.me/+tLXxnvJlzZo0M2Ey'},
    {"id": 1850257894, "name": 'Луцьк', "link": 'https://t.me/+jNKHP_USSJZhNzgy'},
    {"id": 1677904749, "name": 'Киев', "link": 'https://t.me/+cG_xCnSl7thiMzgy'},
    {"id": 1607603790, "name": 'Тернополь', "link": 'https://t.me/+oGriP3680ec1NDVi'},
]

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

for channel_data in default_channels:
    channel_exists = session.query(Channel).filter_by(id=channel_data["id"]).first()

    if not channel_exists:
        new_channel = Channel(**channel_data)
        session.add(new_channel)

session.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
