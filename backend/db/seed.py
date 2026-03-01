from backend.core.security.password import get_password_hash
from backend.modules.user.models import User, UserRole

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


async def create_initial_admin(session: AsyncSession):
    result = await session.execute(select(User).where(User.username == "admin"))
    admin = result.scalar_one_or_none()

    if not admin:
        hashed_pw = get_password_hash("admin")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_pw,
            role=UserRole.ADMIN,
        )
        session.add(admin)
        await session.commit()
