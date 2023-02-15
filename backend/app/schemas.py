from typing import Dict, Optional, Union, List

from pydantic import BaseModel


class NotificationBase(BaseModel):
    message: str


class NotificationIn(NotificationBase):
    template_values: Optional[Dict[str, Union[str, int]]]


class Notification(NotificationBase):
    id: int

    class Config:
        orm_mode = True


class UserNotification(BaseModel):
    user_id: int
    notification_id: int
    read: bool
    notification: Notification


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    notifications: List[UserNotification] = []

    class Config:
        orm_mode = True
