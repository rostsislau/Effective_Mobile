from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.security import create_access_token, verify_password
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalars().first()
    if (
        not user
        or not user.is_active
        or not verify_password(data.password, user.hashed_password)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(
        {"user_id": user.id, "role": user.role.name if user.role else None}
    )
    return {"access_token": token}


@router.post("/logout")
async def logout():
    # просто клиент удаляет токен
    return {"msg": "Successfully logged out"}
