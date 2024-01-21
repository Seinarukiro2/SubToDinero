import logging
from telethon.sync import events
import telethon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_channel_handler(event, create_channel, session):
    logger.info("Пользователь начал процесс добавления нового канала")

    async with event.client.conversation(event.chat_id) as conv:
        await conv.send_message("Введіть дані нового каналу у форматі: id - name - link")

        response = await conv.get_response()

        try:
            input_data = response.text.strip()
            channel_data = input_data.split(' - ')

            if len(channel_data) == 3:
                channel_id, channel_name, channel_link = map(str.strip, channel_data)

                new_channel = create_channel(
                    session, channel_id=channel_id, name=channel_name, link=channel_link)

                await conv.send_message(f"Канал успішно додано: {new_channel.id} - {new_channel.name} - {new_channel.link}")
                logger.info(
                    f"Канал успішно додано: {new_channel.id} - {new_channel.name} - {new_channel.link}")
            else:
                await conv.send_message("Невірний формат. Будь ласка, введіть дані в правильному форматі.")
                logger.warning("Невірний формат введених даних")

        except telethon.errors.rpcerrorlist.TimeoutError:
            await conv.send_message("Час очікування минув. Спробуйте ще раз.")
            logger.warning("Час очікування минув. Спробуйте ще раз.")

        except Exception as e:
            await conv.send_message(f"Сталася помилка: {str(e)}")
            logger.error(f"Сталася помилка: {str(e)}")

        finally:
            session.close()
