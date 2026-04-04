from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.modules.user.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_username(self, username: str):
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id(self, id: int):
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user
