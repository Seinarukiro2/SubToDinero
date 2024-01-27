from telethon import TelegramClient, events
from sqlalchemy.orm import Session
from database import User


async def deactivate_admin_session(
    event: events.NewMessage.Event, client: TelegramClient, session: Session
):
    user_id = event.sender_id
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if user:
        user.is_admin_session_active = False
        session.commit()
        await client.send_message(event.chat_id, "Админская сессия деактивирована.")
    else:
        await client.send_message(
            event.chat_id, "Пользователь не найден в базе данных."
        )
