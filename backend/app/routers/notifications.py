from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..schemas import User, Notification

from ..crud import get_user_notifications

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    dependencies=[],
    responses={404: {"error": "Not Found"}},
)


@router.get("/", response_model=List[Notifications])
async def read_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_notifications = get_user_notifications(db, current_user.id)
    return [un.notification for un in user_notifications]


@router.post("/")
async def notifications():
    pass
