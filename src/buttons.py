from telethon import Button
from database import SessionLocal, Channel

def get_channel_buttons():
    session = SessionLocal()
    channels = session.query(Channel).all()

    # Генерация кнопок: по две кнопки в одном ряду
    buttons = [
        [
            # ТИМУР ТУТ ДОЛЖНЫ БЫТЬ ССЫЛКИ ТО ЕСТЬ СНАЧАЛА ИМЯ КАНАЛА А ПОТОМ ССЫЛКА А ТО ЩАС ЧЕПУХА КАКАЯ ТО
            Button.inline(channel.name, bytes(f'join_channel_{channel.id}', 'utf-8')),
            Button.inline(another_channel.name, bytes(f'join_channel_{another_channel.id}', 'utf-8'))
        ] for channel, another_channel in zip(channels[0::2], channels[1::2])
    ]

    # Проверка на нечетное количество каналов
    if len(channels) % 2 != 0:
        # Добавим одну кнопку для последнего нечетного канала
        last_channel = channels[-1]
        buttons.append([Button.inline(last_channel.name, bytes(f'join_channel_{last_channel.id}', 'utf-8'))])

    # Добавление кнопки "Перевірити підписку"
    check_subscription_button = [Button.inline("Перевірити підписку", b'check_subscription')]
    buttons.append(check_subscription_button)

    session.close()
    return buttons
