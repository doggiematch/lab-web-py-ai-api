import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mi-clave-super-secreta-cambiar-en-produccion")
PORT = int(os.getenv("PORT", 8000))
