from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    full_name: str | None
    email: EmailStr | None


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True
