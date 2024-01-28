from sqlalchemy.orm import aliased
from database import SessionLocal, ToSubscribeChannel, Channel

async def handle_delete_channel(event):
    session = SessionLocal()
    user_id = event.sender_id
    try:
        # Создаем псевдонимы для таблиц
        to_subscribe_alias = aliased(ToSubscribeChannel, name='ToSubscribe')
        channel_alias = aliased(Channel, name='StartChannel')

        # Получаем все каналы из обеих таблиц
        to_subscribe_channels = session.query(to_subscribe_alias).all()
        start_channels = session.query(channel_alias).all()

        # Собираем данные для вывода
        result_text = "Канали для видалення:\n"
        for to_subscribe_channel in to_subscribe_channels:
            result_text += f"(ToSubscribe) - {to_subscribe_channel.id} - {to_subscribe_channel.name}\n"

        for start_channel in start_channels:
            result_text += f"(StartChannel) - {start_channel.id} - {start_channel.name}\n"

        # Отправляем результат пользователю
        await event.respond(result_text)

        # Ожидаем ввода данных о канале
        async with event.client.conversation(event.chat_id) as conv:
            await conv.send_message(
                "Введіть дані каналу для видалення у форматі: ToSubscribe/StartChannel - id"
            )

            response = await conv.get_response()
            data = response.text.strip().split(' - ')

            if len(data) == 2:
                channel_type, channel_id = data[0].strip(), data[1].strip()
                if channel_type == "ToSubscribe":
                    channel = session.query(ToSubscribeChannel).filter(ToSubscribeChannel.id == channel_id).first()
                elif channel_type == "StartChannel":
                    channel = session.query(Channel).filter(Channel.id == channel_id).first()

                if channel:
                    session.delete(channel)
                    session.commit()
                    await event.respond(f"Канал {channel_type} з id {channel_id} успішно видалено.")
                else:
                    await event.respond(f"Канал з id {channel_id} не знайдено.")
            else:
                await event.respond("Невірний формат введених даних.")

    except Exception as e:
        print(f"Error handling delete_channel callback: {e}")
    finally:
        session.close()