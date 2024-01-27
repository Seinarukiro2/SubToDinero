from database import SessionLocal, User, Channel


async def handle_bot_chat_invite_requester(event):
    channel_id = int(event.peer.channel_id)
    user_id = event.user_id
    title = event.invite.title

    if channel_id and user_id and title == "dinero":
        session = SessionLocal()
        print("123")
        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            channel = session.query(Channel).filter(Channel.id == channel_id).first()
            print(channel)
            if channel:
                print("123")
                # Проверим, не подписан ли пользователь уже на этот канал
                if channel not in user.subscribed_channels:
                    print("123")
                    user.subscribed_channels.append(channel)
                    print("123")
                    user.update_subscribed_all()
                    print("123")
                    session.commit()

                    print(f"Пользователь {user_id} подписался на канал {channel_id}")
                else:
                    print(f"Пользователь {user_id} уже подписан на канал {channel_id}")
        else:
            print(f"Пользователь {user_id} не найден в базе данных.")

        session.close()
