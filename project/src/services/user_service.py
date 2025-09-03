from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.security import hash_password, verify_password
from src.models.user import User


# Создание нового пользователя
async def create_user(
    db: AsyncSession, full_name: str, email: str, password: str
) -> User:
    hashed = hash_password(password)
    user = User(full_name=full_name, email=email, hashed_password=hashed)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Получение пользователя по email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# Проверка пароля пользователя
async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
