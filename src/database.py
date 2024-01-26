from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = 'sqlite:///bot_database.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)
Base = declarative_base()

user_channel_association = Table(
    'user_channel_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.telegram_id')),
    Column('channel_id', Integer, ForeignKey('channels.id'))
)

user_subscribe_channel_association = Table(
    'user_subscribe_channel_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.telegram_id')),
    Column('to_subscribe_channel_name', String, ForeignKey('to_subscribe_channels.name'))
)

class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, unique=True, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    phone_number = Column(String, nullable=True)
    first_start_date = Column(DateTime, default=datetime.utcnow)
    source_start = Column(String, nullable=True)
    is_admin_session_active = Column(Boolean, default=False)
    subscribed_all = Column(Boolean, default=False)
    subscribed_channels = relationship(
        "Channel", secondary=user_channel_association, back_populates="subscribers")
    subscribed_to_channels = relationship(
        "ToSubscribeChannel", secondary=user_subscribe_channel_association, back_populates="subscribers")

    def update_subscribed_all(self):
        subscribed_channel_ids = set(channel.id for channel in self.subscribed_channels)
        all_channel_ids = set(channel.id for channel in self.get_all_channels())

        self.subscribed_all = subscribed_channel_ids.issuperset(all_channel_ids)

    def get_all_channels(self):
        all_channels = session.query(Channel).all()
        return all_channels

    def remaining_channels_to_subscribe(self, session):
        all_channel_ids = set(channel.name for channel in session.query(ToSubscribeChannel).all())
        subscribed_channel_ids = set(channel.name for channel in self.subscribed_to_channels)
        remaining_channels = len(all_channel_ids - subscribed_channel_ids)
        return remaining_channels


class ToSubscribeChannel(Base):
    __tablename__ = 'to_subscribe_channels'

    name = Column(String, primary_key=True, unique=True, index=True)
    link = Column(String)
    subscribers = relationship(
        "User", secondary=user_subscribe_channel_association, back_populates="subscribed_to_channels")


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    link = Column(String)

    subscribers = relationship(
        "User", secondary=user_channel_association, back_populates="subscribed_channels")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
