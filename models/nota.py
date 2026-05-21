from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NotaEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    contenido: str = Field(min_length=1)


class NotaSalida(BaseModel):
    id: int
    titulo: str
    contenido: str
    usuario_id: int
    creada_en: datetime


class NotaActualizar(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None