from telethon.sync import events
from database import User, SessionLocal
import logging



async def handle_set_admin(event):
    user_id = event.sender_id

    try:
        # Создаем объект сессии
        session = SessionLocal()

        # Получаем пользователя из базы данных
        db_user = session.query(User).filter(User.telegram_id == user_id).first()

        if db_user:
            if db_user.is_admin_session_active:
                await event.respond("Админская сессия уже активирована.")
            else:
                await event.respond("Введите пароль для активации админской сессии.")

                async def check_password(event):
                    # Здесь вы можете реализовать проверку пароля
                    # Например, сравнение с хэшированным паролем в базе данных
                    # Пока просто допустим, что пароль равен "admin_password"
                    return event.message.text == "admin_password"

                # Регистрируем обработчик события для ожидания ввода пароля
                @event.client.on(events.NewMessage(from_users=user_id, incoming=True))
                async def wait_for_password(response_event):
                    if await check_password(response_event):
                        db_user.is_admin_session_active = True
                        session.commit()
                        await response_event.respond("Админская сессия активирована.")
                        # Отключаем обработчик после успешной активации админской сессии
                        event.client.remove_event_handler(wait_for_password)
                    else:
                        await response_event.respond("Пароль неверен.")
                        event.client.remove_event_handler(wait_for_password)

                # Дожидаемся ответа пользователя
                await event.client.run_until_disconnected()

        else:
            await event.respond("Вы еще не зарегистрированы. Используйте /start для начала.")
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /set_admin: {e}")
    finally:
        # Закрываем сессию
        session.close()
