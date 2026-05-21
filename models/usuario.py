from pydantic import BaseModel, EmailStr, Field


class UsuarioRegistro(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioSalida(BaseModel):
    id: int
    email: EmailStr