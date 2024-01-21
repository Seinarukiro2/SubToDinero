from sqlalchemy.orm import Session
from database import Channel


def get_channel_by_id(db: Session, channel_id: int):
    return db.query(Channel).filter(Channel.id == channel_id).first()


def get_channel_by_name(db: Session, channel_name: str):
    return db.query(Channel).filter(Channel.name == channel_name).first()


def create_channel(db: Session, channel_id: int, name: str, link: str):
    channel = Channel(id=channel_id, name=name, link=link)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


def get_all_channels(db: Session):
    return db.query(Channel).all()
