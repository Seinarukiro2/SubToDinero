from telethon import Button


async def send_subscription_buttons(event, user, session):
    try:
        if user:
            to_subscribe_channels = user.remaining_channels_to_subscribe(session)
            buttons = [
                [Button.url(text=channel.name, url=channel.link)]
                for channel in to_subscribe_channels
            ]
            
            # Добавляем отдельный вложенный список для дополнительной кнопки
            buttons.append([Button.inline("Перевiрка пiдписки", b"check_subscription_all")])

            await event.respond(
                "Канали доступні для підписки. За кожну підписку ви отримаєте 5 грн пiсля перевiрки.",
                buttons=buttons,
            )
        else:
            await event.respond("Помилка: користувач не знайдений в базі даних.")
    finally:
        await event.delete()
        session.close()
