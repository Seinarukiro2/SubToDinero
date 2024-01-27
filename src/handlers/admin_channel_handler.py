# handlers/admin_channel_handler.py

from telethon.sync import events
from database import Channel, SessionLocal
import logging

# Настройка конфигурации логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()],
)


async def handle_add_admin_channel(event, client):
    user_id = event.sender_id

    try:
        # Создаем объект сессии
        session = SessionLocal()

        # Отправляем запрос на ввод ссылки на канал

        # Создаем объект конверсации
        async with event.client.conversation(event.chat_id) as conv:
            try:
                await conv.send_message("Введите ссылку на канал.")
                # Ждем ввода пользователя в течение 10 секунд
                response = await conv.get_response(timeout=10)
                print(response)
                # Проверяем, является ли бот администратором этого канала
                try:
                    channel_link = response.text.strip()

                    # Получаем информацию о канале
                    entity = await client.get_participants(
                        entity=channel_username, aggressive=True
                    )

                    # Проверяем, является ли бот администратором канала
                    if entity:
                        # Если бот администратор, добавляем информацию о канале в базу данных
                        new_channel = AdminChannel(
                            channel_link=entity.username, channel_name=entity.title
                        )
                        session.add(new_channel)
                        session.commit()
                        logging.info(
                            f"Канал успешно добавлен: ID={new_channel.id}, "
                            f"Ссылка={new_channel.channel_link}, Имя={new_channel.channel_name}"
                        )
                        await event.respond("Канал успешно добавлен.")
                    else:
                        # Если бот не администратор, сообщаем, что его нужно добавить в администраторы канала
                        logging.info(
                            f"Бот не является администратором канала: Ссылка={channel_link}"
                        )
                        await event.respond("Добавьте бота в администраторы канала.")
                except Exception as e:
                    logging.error(f"Ошибка при получении информации о канале: {e}")
                    await event.respond(
                        "Произошла ошибка. Пожалуйста, убедитесь, что введена правильная ссылка на канал."
                    )

            except TimeoutError:
                logging.warning("Время ожидания ввода ссылки на канал вышло.")

    except Exception as e:
        logging.error(f"Ошибка при обработке команды /add_admin_channel: {e}")
    finally:
        # Закрываем сессию
        session.close()
