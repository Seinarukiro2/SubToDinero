# menu_builder.py

from telethon.tl.custom import Button, Message


async def build_user_menu(user):
    username = user.username if user.username else "Немає імені користувача"
    balance = user.subscribed_to_channels * 4  # Assuming each channel costs 4 in currency

    remaining_channels = len(user.subscribed_to_channels)  # Assuming a maximum of 10 channels

    menu_text = (
        f"Ласкаво просимо, {username}!\n"
        f"Ваш баланс: {balance} грн\n"
        f"Підписані канали: {user.subscribed_to_channels}\n"
        f"Канали для підписки: {remaining_channels}\n\n"
        "Оберіть дію:"
    )

    # Creating buttons with callback data
    balance_button = Button.inline("Показати баланс", b"show_balance")
    subscribe_button = Button.inline("Почати підписуватися", b"start_subscribing")
    support_button = Button.inline("Підтримка", b"support")

    # Creating the Telegram message with the text and buttons

    message=menu_text,
    buttons=[[balance_button, subscribe_button], [support_button]]


    return message, buttons
