from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from models.usuario import (
    UsuarioRegistro,
    UsuarioLogin
)

from auth.jwt import crear_token


router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"])

usuarios = []
contador_usuarios = 1

#registro
@router.post("/registro")
def registro(usuario: UsuarioRegistro):
    global contador_usuarios

    for u in usuarios:
        if u["email"] == usuario.email:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

    password_hash = pwd_context.hash(usuario.password)

    nuevo_usuario = {
        "id": contador_usuarios,
        "email": usuario.email,
        "password": password_hash
    }

    usuarios.append(nuevo_usuario)

    contador_usuarios += 1

    return {
        "mensaje": "Usuario registrado"
    }

#login
@router.post("/login")
def login(usuario: UsuarioLogin):

    for u in usuarios:

        password_correcta = pwd_context.verify(
            usuario.password,
            u["password"]
        )

        if u["email"] == usuario.email and password_correcta:

            token = crear_token({
                "usuario_id": u["id"]
            })

            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(
        status_code=401,
        detail="Credenciales incorrectas"
    )