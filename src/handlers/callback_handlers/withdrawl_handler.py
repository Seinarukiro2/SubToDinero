from telethon.sync import events
from database import User, SessionLocal
from telethon.tl.custom import Button


async def handle_withdrawal_balance(event, client):
    user_id = event.sender_id
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            if user.balance >= 100:

                await event.respond("Ваш запит на вивід відправлено.")
                user.balance = 0
                session.commit()
            else:

                await event.respond("Вивід доступний від 100 грн.")
        else:
            await event.respond("Помилка: користувача не знайдено в базі даних.")
    except Exception as e:

        print(f"Помилка при обробці запиту на вивід: {e}")
    finally:

        session.close()
