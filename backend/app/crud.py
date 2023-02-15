from typing import Optional

from sqlalchemy.orm import Session

from . import auth, models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = auth.fake_hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_notification(
    db: Session, notification: schemas.NotificationIn
) -> models.Notification:
    message = notification.message
    if notification.template_values:
        message = message.format(**notification.template_values)

    db_notification = models.Notification(message)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def create_user_notification(
    db: Session, user: models.User, notification: models.Notification
):
    db_user_notification = models.UserNotification(read=False)
    db_user_notification.notification = notification
    user.notifications.append(db_user_notification)
    db.add(db_user_notification)
    db.add(user)
    db.commit()
    db.refresh(db_user_notification)
    db.refresh(user)
    return db_user_notification


def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.UserNotification)
        .filter(models.User.id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
