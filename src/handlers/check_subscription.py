from database import SessionLocal, User


async def check_subscription(user_id):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.telegram_id == user_id).first()

        if user:
            if user.subscribed_all or user.is_admin_session_active:
                return True
            else:
                return False
        else:
            return False

    finally:
        session.close()
