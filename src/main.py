from telethon.sync import TelegramClient, events
from database import User, SessionLocal
import telethon
from telethon.tl import functions
from telethon.tl.types import PeerChat, PeerChannel
from handlers.check_subscription import check_subscription
from telethon.sync import events
from database import SessionLocal, User
from handlers.start_handler import handle_start
from handlers.admin_handler import handle_set_admin
from handlers.admin_channel_handler import handle_add_admin_channel
from decorators.admin_decorator import admin_session_required
import json


with open('secrets.json', 'r') as file:
    secrets = json.load(file)

API_ID = secrets['API_ID']
API_HASH = secrets['API_HASH']
BOT_TOKEN = secrets['BOT_TOKEN']

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Обработка команды /start
@client.on(events.NewMessage(pattern='/start'))
async def handle_start_wrapper(event):
    await handle_start(event)

@client.on(events.NewMessage(pattern='/set_admin'))
async def set_admin_handler_wrapper(event):
    await handle_set_admin(event)

@client.on(events.NewMessage(pattern='/add_admin_channel'))
@admin_session_required
async def handle_add_admin_channel_wrapper(event):
    await handle_add_admin_channel(event, client)


@client.on(events.Raw(telethon.types.UpdateBotChatInviteRequester))
async def approve(e):
    channel_id = int(e.peer.channel_id)  
    user_id = e.user_id
    title = e.invite.title

    if channel_id and user_id and title == 'dinero':
        session = SessionLocal()

        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            channel_fields = {
                1949156593: 'subscribed_hmelnytskyi',
                1850257894: 'subscribed_lutsk',
                1677904749: 'subscribed_kiev',
                1607603790: 'subscribed_ternopil',
            }

            if channel_id in channel_fields:

                setattr(user, channel_fields[channel_id], True)

                user.update_subscribed_all()
                session.commit()

                print(f"Пользователь {user_id} подписался на канал {channel_id}")

        session.close()


@client.on(events.CallbackQuery(data=b'check_subscription'))
async def callback_handler(event):
    user_id = event.sender_id

    if check_subscription(user_id):
        await event.respond("Я маленький гвинтик")
    else:
        await event.respond("Підпишіться на всі канали, щоб продовжити.")

if __name__ == '__main__':
    print("Бот запущен. Для завершения работы используйте Ctrl+C.")
    client.run_until_disconnected()
