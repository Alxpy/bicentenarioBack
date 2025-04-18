import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from src.presentation.controllers.auth_controller import auth_router
from src.presentation.controllers.biblioteca_controller import biblioteca_router
from src.presentation.controllers.categoriaNoticia_controller import category_router
from src.presentation.controllers.categoria_historia_controller import history_category_router
from src.presentation.controllers.cultura_controller import culture_router
from src.presentation.controllers.tipoDocumento_controller import document_type_router
from src.presentation.controllers.email_controller import email_router
from src.presentation.controllers.file_controller import file_router
from src.presentation.controllers.historia_controller import historia_router
from src.presentation.controllers.ubicacion_controller import location_router
from src.presentation.controllers.multimedia_cultura_controller import multimedia_cultura_router
from src.presentation.controllers.multimedia_historia_controller import multimedia_historia_router
from src.presentation.controllers.multimedia_controller import multimedia_router
from src.presentation.controllers.noticia_controller import news_router
from src.presentation.controllers.presidente_controller import president_router
from src.presentation.controllers.rol_controller import rol_router
from src.presentation.controllers.user_controller import user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(biblioteca_router)
app.include_router(history_category_router)
app.include_router(category_router)
app.include_router(culture_router)
app.include_router(document_type_router)
app.include_router(email_router)
app.include_router(file_router)
app.include_router(historia_router)
app.include_router(location_router)
app.include_router(multimedia_cultura_router)
app.include_router(multimedia_historia_router)
app.include_router(multimedia_router)
app.include_router(news_router)
app.include_router(president_router)
app.include_router(rol_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug"
    )