
from database import SessionLocal, ToSubscribeChannel, User
from telethon.tl import types
from telethon.tl.custom import Button

async def handle_add_tosubscribe_channel(event):
    user_id = event.sender_id

    # Проверяем, является ли пользователь адміністратором
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if not user or not user.is_admin_session_active:
            await event.respond("Ви повинні бути адміністратором для виконання цієї команди.")
            return

        async with event.client.conversation(event.chat_id) as conv:
            await conv.send_message("Введіть дані нового каналу у форматі: name - link")

            response = await conv.get_response()
            channel_data = response.text.strip().split(" - ")

            if len(channel_data) != 2:
                await event.respond("Неправильний формат введення. Будь ласка, використовуйте формат: name - link")
                return

            channel_name, channel_link = channel_data
            new_channel = ToSubscribeChannel(name=channel_name, link=channel_link)
            session.add(new_channel)
            session.commit()

            # Отправляем повідомлення всім користувачам
            subscribed_users = session.query(User).all()
            for user in subscribed_users:
                try:
                    button_url = Button.url(channel_name, channel_link)
                    button_check_subscription = Button.inline("Перевірити підписку", data=b"check_subscription_all")

                    await event.client.send_message(
                        user.telegram_id,
                        f"Новий канал {channel_name} доступний для пiдписки!",
                        buttons=[[button_url], [button_check_subscription]]
                    )
                except Exception as e:
                    print(f"Помилка при надсиланні повідомлення користувачу {user.telegram_id}: {e}")
    except Exception as e:
        print(f"Помилка при додаванні каналу: {e}")
    finally:
        session.close()
