from jose import jwt, JWTError # jose crea y verifica tokens, es una librería
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from config import SECRET_KEY
from datetime import datetime, timedelta, UTC


ALGORITHM = "HS256" #algoritmo de jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #oauth2 es para la autenticación/autorización en apis, fastapi lo usa para esperar un token bearer y proteger rutas


def crear_token(datos: dict):
    datos_token = datos.copy()
    expiracion = datetime.now(UTC) + timedelta(hours=2) #datetime.utcnow() no se pudo usar porque está obsoleto en python, así que hay que sustituirlo, mejor, por now(utc)
    datos_token.update({"exp": expiracion})
    return jwt.encode(datos_token, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = datos.get("usuario_id")

        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")