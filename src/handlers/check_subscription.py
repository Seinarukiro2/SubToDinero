from database import SessionLocal, User

def check_subscription(user_id):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            if user.subscribed_all or user.is_admin_session_active:
                return True  # Пользователь подписан на все каналы
            else:
                return False  # Пользователь не подписан на все каналы
        else:
            return False  # Пользователь не найден в базе данных

    finally:
        session.close()
