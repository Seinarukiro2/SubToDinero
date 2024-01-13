from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'sqlite:///bot_database.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True, nullable=True)
    phone_number = Column(String, nullable=True)
    first_start_date = Column(DateTime, default=datetime.utcnow)
    source_start = Column(String, nullable=True)
    is_admin_session_active = Column(Boolean, default=False)

    # Добавляем поля подписки на каналы
    subscribed_hmelnytskyi = Column(Boolean, default=False)
    subscribed_lutsk = Column(Boolean, default=False)
    subscribed_kiev = Column(Boolean, default=False)
    subscribed_ternopil = Column(Boolean, default=False)

    # Добавляем поле, отслеживающее подписку на все каналы
    subscribed_all = Column(Boolean, default=False)

    # Обновляем subscribed_all при изменении других полей
    def update_subscribed_all(self):
        self.subscribed_all = all(getattr(self, f"subscribed_{channel_name}") for channel_name in ["hmelnytskyi", "lutsk", "kiev", "ternopil"])

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    link = Column(String)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Дефолтные записи перед созданием таблиц
default_channels = [
    Channel(id=1949156593, name='Хмельницкий', link='https://t.me/+tLXxnvJlzZo0M2Ey'),
    Channel(id=1850257894, name='Луцьк', link='https://t.me/+jNKHP_USSJZhNzgy'),
    Channel(id=1677904749, name='Киев', link='https://t.me/+cG_xCnSl7thiMzgy'),
    Channel(id=1607603790, name='Тернополь', link='https://t.me/+oGriP3680ec1NDVi'),
]

# Создаем объект сессии и добавляем дефолтные записи
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
session.add_all(default_channels)
session.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
