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
from handlers.add_channel_handler import add_channel_handler
from decorators.admin_decorator import admin_session_required
from handlers.deactivate_admin_handler import deactivate_admin_session
import json
from functions.channel_table_operations import create_channel
from database import Channel

with open('secrets.json', 'r') as file:
    secrets = json.load(file)

API_ID = secrets['API_ID']
API_HASH = secrets['API_HASH']
BOT_TOKEN = secrets['BOT_TOKEN']

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


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

@client.on(events.NewMessage(pattern='/deactivate'))
async def handle_deactivate_admin_session(event):
    with SessionLocal() as session:
        await deactivate_admin_session(event, client, session)

@client.on(events.Raw(telethon.types.UpdateBotChatInviteRequester))
async def approve(e):
    channel_id = int(e.peer.channel_id)
    user_id = e.user_id
    title = e.invite.title

    if channel_id and user_id and title == 'dinero':
        session = SessionLocal()
        print('123')
        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            channel = session.query(Channel).filter(Channel.id == channel_id).first()
            print(channel)
            if channel:
                print('123')
                # Проверим, не подписан ли пользователь уже на этот канал
                if channel not in user.subscribed_channels:
                    print('123')
                    user.subscribed_channels.append(channel)
                    print('123')
                    user.update_subscribed_all()
                    print('123')
                    session.commit()

                    print(f"Пользователь {user_id} подписался на канал {channel_id}")
                else:
                    print(f"Пользователь {user_id} уже подписан на канал {channel_id}")
        else:
            print(f"Пользователь {user_id} не найден в базе данных.")

        session.close()


@client.on(events.NewMessage(pattern='/add_channel'))
async def handle_add_channel(event):
    await add_channel_handler(event, create_channel, SessionLocal())


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
