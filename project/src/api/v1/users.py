from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.security import hash_password
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.user import UserCreate, UserOut, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )
    return new_user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_async_session)
):
    result = await db.get(User, user_id)
    if not result or not result.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    if user.full_name:
        result.full_name = user.full_name
    if user.email:
        result.email = user.email
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.get(User, user_id)
    if not result or not result.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    result.is_active = False
    await db.commit()
    return result


# Эндпоинт получения всех пользователей
@router.get("/all", response_model=List[UserOut])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
