from fastapi import HTTPException, status
from datetime import datetime

from backend.core.event_bus import EventBus
from backend.core.security.password import get_password_hash, verify_password

from backend.modules.user.schemas import UserCreate, UserLogin
from backend.modules.user.events import UserEvents
from backend.modules.user.models import User

from backend.modules.user.repository import UserRepository




class UserService:
    def __init__(self, repo: UserRepository, event_bus: EventBus):
        self.repo = repo
        self.event_bus = event_bus

    async def create_user(self, user_in: UserCreate):
        existing = await self.repo.get_by_username(user_in.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        user = User(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
        )
        await self.repo.create(user)

        await self.event_bus.publish(
            UserEvents.CREATED, {"user_id": user.id, "username": user.username}
        )
        return user

    async def login_user(self, user_in: UserLogin, ip: str = "unknown"):
        user = await self.repo.get_by_username(user_in.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password or login",
            )

        if not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password or login",
            )

        await self.event_bus.publish(
            UserEvents.LOGGEN_IN,
            {
                "user_id": user.id,
                "username": user.username,
                "ip": ip,
                "ts": datetime.utcnow().isoformat(),
            },
        )
        return user
