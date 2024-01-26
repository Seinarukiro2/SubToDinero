# menu_texts.py
from telethon import Button

async def get_user_menu_text(event, user, session):
    username = user.username if user.username else "Немає імені користувача"
    balance = len(user.subscribed_to_channels) * 4  # Assuming each channel costs 4 in currency
    remaining_channels = user.remaining_channels_to_subscribe(session)

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

    buttons=[[balance_button], [subscribe_button], [support_button]]

    await event.respond(menu_text, buttons=buttons)
