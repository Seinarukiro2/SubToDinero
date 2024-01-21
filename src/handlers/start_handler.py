# start_handler.py

from telethon.sync import events
from database import User, SessionLocal
from datetime import datetime
import logging
from handlers.menu_texts import SUBSCRIPTION_MENU_TEXT
from buttons import get_channel_buttons
from telethon.tl import types
from menus import build_user_menu
from telethon.tl.custom import Button
# Настройка конфигурации логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


async def handle_start(event):
    user_id = event.sender_id
    username = event.sender.username

    try:
        # Парсим информацию из команды /start
        command_text = event.raw_text.split(' ', 1)[1] if len(
            event.raw_text.split(' ', 1)) > 1 else None
        phone_number = event.contact.phone_number if event.contact else None
        source_start = command_text.split(
            '_')[1] if command_text and command_text.startswith('r_') else None

        # Создаем объект сессии
        session = SessionLocal()

        db_user = session.query(User).filter(User.telegram_id == user_id).first()

        if not db_user:
            new_user = User(
                telegram_id=user_id,
                username=username,
                phone_number=phone_number,
                source_start=source_start
            )
            session.add(new_user)
            session.commit()
            # Обновляем состояние объекта пользователя в сессии
            session.refresh(new_user)

            # Логируем информацию о создании нового пользователя
            logging.info(f"Новый пользователь: Telegram ID={new_user.telegram_id}, "
                         f"Время создания={new_user.first_start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            logging.info(
                f"Пользователь уже существует: Telegram ID={db_user.telegram_id}")

        if db_user and db_user.subscribed_all or db_user and db_user.is_admin_session_active:
            # Если пользователь подписан на все каналы, выводим сообщение с меню/кнопками
            user = db_user
            username = user.username if user.username else "Немає імені користувача"
            balance = len(user.subscribed_to_channels) * 4  # Assuming each channel costs 4 in currency
            
            remaining_channels = user.remaining_channels_to_subscribe

            menu_text = (
                f"Ласкаво просимо, {username}!\n"
                f"Ваш баланс: {balance} грн\n"
                f"Підписані канали: {len(user.subscribed_to_channels)}\n"
                f"Канали для підписки: {remaining_channels}\n\n"
                "Оберіть дію:"
            )

            # Creating buttons with callback data
            balance_button = Button.inline("Вивести баланс", b"withdrawl_balance")
            subscribe_button = Button.inline("Почати підписуватися", b"start_subscribing")
            support_button = Button.inline("Підтримка", b"support")

            # Creating the Telegram message with the text and buttons

            message=menu_text

            buttons=[[balance_button], [subscribe_button], [support_button]]
            await event.respond(message, buttons=buttons)
            # Здесь добавим код для вывода кнопок с меню (пока заглушка)
        else:
            # Если пользователь не подписан на все каналы, выводим просьбу подписаться и кнопки с каналами
            await event.respond(
                SUBSCRIPTION_MENU_TEXT.get('uk'),
                buttons=get_channel_buttons()
            )
            # Здесь добавим код для вывода кнопок с каналами (пока заглушка)

    except Exception as e:
        logging.error(f"Ошибка при обработке команды /start: {e}")
    finally:
        # Закрываем сессию
        session.close()
