from telethon.sync import TelegramClient, events
from database import User, SessionLocal
import telethon
from telethon.tl import functions

from handlers.start_handler import handle_start
from handlers.admin_handler import handle_set_admin
from handlers.admin_channel_handler import handle_add_admin_channel
from decorators.admin_decorator import admin_session_required
API_ID = 7248451
API_HASH = 'db9b16eff233ee8dfd7c218138cb2e10'
BOT_TOKEN = '6988850539:AAHy1wR9-PtG44VuY0E8FKddQWHtF2RBKMA'

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


from telethon.tl.types import PeerChat, PeerChannel

@client.on(events.Raw(telethon.types.UpdateBotChatInviteRequester))
async def approve(e):
    print('кто-то хочет зайти')
    print(e)


if __name__ == '__main__':
    print("Бот запущен. Для завершения работы используйте Ctrl+C.")
    client.run_until_disconnected()
