from functools import wraps
from telethon.sync import events
from database import User, SessionLocal


def admin_session_required(func):
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        user_id = event.sender_id

        try:
            # Создаем объект сессии
            session = SessionLocal()

            # Получаем пользователя из базы данных
            db_user = session.query(User).filter(User.telegram_id == user_id).first()

            if db_user and db_user.is_admin_session_active:
                return await func(event, *args, **kwargs)
            else:
                await event.respond(
                    "Админская сессия не активирована. Используйте /set_admin для активации."
                )
        except Exception as e:
            print(f"Ошибка при проверке админской сессии: {e}")
        finally:
            # Закрываем сессию
            session.close()

    return wrapper
