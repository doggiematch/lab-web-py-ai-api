from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from models.nota import (
    NotaEntrada,
    NotaSalida,
    NotaActualizar
)

from auth.jwt import verificar_token


router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)

notas = []
contador_notas = 1

#crear nota
@router.post("")
def crear_nota(
    nota: NotaEntrada,
    usuario_id: int = Depends(verificar_token)
):
    global contador_notas

    nueva_nota = {
        "id": contador_notas,
        "titulo": nota.titulo,
        "contenido": nota.contenido,
        "usuario_id": usuario_id,
        "creada_en": datetime.now()
    }

    notas.append(nueva_nota)

    contador_notas += 1

    return nueva_nota

#lista notas
@router.get("")
def listar_notas(
    buscar: str = None,
    usuario_id: int = Depends(verificar_token)
):

    resultado = [
        nota for nota in notas
        if nota["usuario_id"] == usuario_id
    ]

    if buscar:
        resultado = [
            nota for nota in resultado
            if buscar.lower() in nota["contenido"].lower()
        ]

    return resultado

#obener una nota
@router.get("/{id}")
def obtener_nota(
    id: int,
    usuario_id: int = Depends(verificar_token)
):

    for nota in notas:

        if (
            nota["id"] == id and
            nota["usuario_id"] == usuario_id
        ):
            return nota

    raise HTTPException(
        status_code=404,
        detail="Nota no encontrada"
    )

#editar una nota
@router.put("/{id}")
def editar_nota(
    id: int,
    datos: NotaActualizar,
    usuario_id: int = Depends(verificar_token)
):

    for nota in notas:

        if (
            nota["id"] == id and
            nota["usuario_id"] == usuario_id
        ):

            if datos.titulo is not None:
                nota["titulo"] = datos.titulo

            if datos.contenido is not None:
                nota["contenido"] = datos.contenido

            return nota

    raise HTTPException(
        status_code=404,
        detail="Nota no encontrada"
    )

#borrar una nota
@router.delete("/{id}")
def eliminar_nota(
    id: int,
    usuario_id: int = Depends(verificar_token)
):

    for nota in notas:

        if (
            nota["id"] == id and
            nota["usuario_id"] == usuario_id
        ):

            notas.remove(nota)

            return {
                "mensaje": "Nota eliminada"
            }

    raise HTTPException(
        status_code=404,
        detail="Nota no encontrada"
    )
