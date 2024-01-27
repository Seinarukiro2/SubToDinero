# start_handler.py

from telethon.sync import events
from database import User, SessionLocal
from datetime import datetime
import logging
from handlers.menu_texts import SUBSCRIPTION_MENU_TEXT
from buttons import get_channel_buttons
from telethon.tl import types
from menus import get_user_menu_text
from telethon.tl.custom import Button

# Настройка конфигурации логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()],
)


async def handle_start(event, client):
    user_id = event.sender_id
    username = event.sender.username

    try:
        command_text = (
            event.raw_text.split(" ", 1)[1]
            if len(event.raw_text.split(" ", 1)) > 1
            else None
        )
        phone_number = event.contact.phone_number if event.contact else None
        source_start = (
            command_text.split("_")[1]
            if command_text and command_text.startswith("r_")
            else None
        )

        session = SessionLocal()

        db_user = session.query(User).filter(User.telegram_id == user_id).first()

        if not db_user:
            new_user = User(
                telegram_id=user_id,
                username=username,
                phone_number=phone_number,
                source_start=source_start,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            referal_message = event.message.message.split(" ")
            if len(referal_message) > 1:
                ref_link_owner = (
                    session.query(User)
                    .filter(User.telegram_id == referal_message[1])
                    .first()
                )
                if ref_link_owner:
                    ref_link_owner.balance += 10
                    new_user.balance += 10
                    session.commit()
                    await client.send_message(
                        types.PeerUser(ref_link_owner.telegram_id),
                        "Ви отримали +10 до балансу за реферала",
                    )
                    await event.respond("Ви отримали +10 до балансу вiд реферала")
            logging.info(
                f"Новый пользователь: Telegram ID={new_user.telegram_id}, "
                f"Время создания={new_user.first_start_date.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            logging.info(
                f"Пользователь уже существует: Telegram ID={db_user.telegram_id}"
            )

        if (
            db_user
            and db_user.subscribed_all
            or db_user
            and db_user.is_admin_session_active
        ):
            await get_user_menu_text(event=event, user=db_user, session=session)
        else:
            await event.respond(
                SUBSCRIPTION_MENU_TEXT.get("uk"), buttons=get_channel_buttons()
            )

    except Exception as e:
        logging.error(f"Ошибка при обработке команды /start: {e}")
    finally:
        session.close()
