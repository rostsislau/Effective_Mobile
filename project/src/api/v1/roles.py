from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.session import get_async_session
from src.models.role import Role
from src.schemas.role import RoleOut  # создадим простую схему вывода

router = APIRouter(prefix="/role", tags=["Role"])


# Эндпоинт для списка ролей
@router.get("/", response_model=list[RoleOut])
async def list_roles(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return roles


# Эндпоинт для создания роли
@router.post("/", response_model=RoleOut)
async def create_role(name: str, db: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли роль с таким именем
    result = await db.execute(select(Role).where(Role.name == name))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(status_code=400, detail="Роль уже существует")

    role = Role(name=name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role
