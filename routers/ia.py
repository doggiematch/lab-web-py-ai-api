from fastapi import APIRouter, Depends

from auth.jwt import verificar_token
from routers.notas import notas


router = APIRouter(
    prefix="/api",
    tags=["IA"]
)

historial_chat = {}

@router.post("/chat")
def chat(
    mensaje: dict,
    usuario_id: int = Depends(verificar_token)
):

    session_id = mensaje.get("session_id")
    texto = mensaje.get("mensaje")

    if session_id not in historial_chat:
        historial_chat[session_id] = []

    historial_chat[session_id].append({
        "usuario": texto
    })

    respuesta = f"Respuesta IA simulada para: {texto}"

    historial_chat[session_id].append({
        "ia": respuesta
    })

    return {
        "respuesta": respuesta
    }

@router.get("/chat/history/{session_id}")
def historial(
    session_id: str,
    usuario_id: int = Depends(verificar_token)
):

    return historial_chat.get(session_id, [])

@router.get("/search")
def buscar_notas(
    q: str,
    usuario_id: int = Depends(verificar_token)
):

    resultado = []

    for nota in notas:

        if (
            nota["usuario_id"] == usuario_id and
            q.lower() in nota["contenido"].lower()
        ):

            resultado.append(nota)

    return resultado

@router.get("/context")
def contexto(
    usuario_id: int = Depends(verificar_token)
):

    return {
        "api": "Sistema IA-ready",
        "capacidades": [
            "chat",
            "busqueda",
            "historial",
            "notas"
        ]
    }
