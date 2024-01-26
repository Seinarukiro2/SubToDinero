from telethon.sync import TelegramClient, events
from telethon.tl import functions, types
from database import SessionLocal, User, Channel
from handlers.check_subscription import check_subscription
from handlers.start_handler import handle_start
from handlers.admin_handler import handle_set_admin
from handlers.admin_channel_handler import handle_add_admin_channel
from handlers.add_channel_handler import add_channel_handler
from decorators.admin_decorator import admin_session_required
from handlers.deactivate_admin_handler import deactivate_admin_session
from handlers.channel_join_request_handler import handle_bot_chat_invite_requester
from functions.channel_table_operations import create_channel
import json

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

@client.on(events.CallbackQuery(pattern=b'start_subscribing'))
async def handle_start_subscribing(event):
    pass

@client.on(events.Raw(types.UpdateBotChatInviteRequester))
async def approve(e):
    await handle_bot_chat_invite_requester(e)

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
