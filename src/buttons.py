from telethon import Button
from database import SessionLocal, Channel


def get_channel_buttons():
    session = SessionLocal()
    channels = session.query(Channel).all()

    # Генерация кнопок: по две кнопки в одном ряду
    buttons = [
        [
            Button.url(channel.name, channel.link),
            Button.url(another_channel.name, another_channel.link),
        ]
        for channel, another_channel in zip(channels[0::2], channels[1::2])
    ]

    if len(channels) % 2 != 0:

        last_channel = channels[-1]
        buttons.append([Button.url(last_channel.name, last_channel.link)])

    # Добавление кнопки "Перевірити підписку"
    check_subscription_button = [
        Button.inline("Перевірити підписку", b"check_subscription")
    ]
    buttons.append(check_subscription_button)

    session.close()
    return buttons
