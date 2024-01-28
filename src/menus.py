# menu_texts.py
from telethon import Button


async def get_user_menu_text(event, user, session):
    username = user.username if user.username else "Немає імені користувача"
    balance = (
        len(user.subscribed_to_channels) * 4
    )  # Assuming each channel costs 4 in currency
    remaining_channels = user.remaining_channels_to_subscribe(session)

    menu_text = (
        f"Ласкаво просимо, {username}!\n"
        f"Ваш баланс: {balance + user.balance} грн\n"
        f"Підписані канали: {len(user.subscribed_to_channels)}\n"
        f"Канали для підписки: {len(remaining_channels)}\n\n"
        "Оберіть дію:"
    )

    # Creating buttons with callback data
    balance_button = Button.inline("Вивести баланс", b"withdrawl_balance")
    subscribe_button = Button.inline("Почати підписуватися", b"start_subscribing")
    support_button = Button.inline("Підтримка", b"support")
    referal_button = Button.inline("Рефералка", b"ref_link")

    buttons = [[balance_button], [subscribe_button], [support_button], [referal_button]]

    await event.respond(menu_text, buttons=buttons)


async def get_admin_menu_text(event):
    admin_menu_text = "Ласкаво просимо в адмін-меню!\nОберіть дію:"

    # Создание кнопок для админ-меню
    add_start_channel_button = Button.inline("Додати старт-канал", b"add_start_channel")
    add_channel_button = Button.inline("Додати канал", b"add_channel")
    delete_channel = Button.inline("Видалити канал", b"delete_channel")
    export_database_button = Button.inline("Експорт бази даних", b"export_database")

    buttons = [
        [add_start_channel_button],
        [add_channel_button],
        [delete_channel],
        [export_database_button],
    ]

    await event.respond(admin_menu_text, buttons=buttons)
