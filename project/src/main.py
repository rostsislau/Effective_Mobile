from fastapi import FastAPI

from src.api.v1 import auth, roles, users
from src.db.base import Base
from src.db.session import engine

app = FastAPI(title="User Management API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(roles.router)
