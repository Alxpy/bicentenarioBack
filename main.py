import logging
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.controllers.user_controller import user_router
from src.presentation.controllers.auth_controller import auth_controller
from src.presentation.controllers.email_controller import email_controller
from src.presentation.controllers.categoriaNoticia_controller import category_controller
from src.presentation.controllers.noticia_controller import news_controller
from src.presentation.controllers.tipoDocumento_controller import document_type_controller
from src.presentation.controllers.biblioteca_controller import biblioteca_controller
from src.presentation.controllers.ubicacion_controller import location_controller
from src.presentation.controllers.cultura_controller import culture_controller
from src.presentation.controllers.presidente_controller import presidente_controller
from src.presentation.controllers.rol_controller import rol_controller
from src.presentation.controllers.multimedia_controller import multimedia_controller
from src.presentation.controllers.multimedia_historia_controller import multimedia_historia_controller
from src.presentation.controllers.multimedia_cultura_controller import multimedia_cultura_controller
from src.presentation.controllers.categoria_historia_controller import categoria_historia_controller
from src.presentation.controllers.historia_controller import historia_controller
from src.presentation.controllers.file_controller import routerfile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_controller)
app.include_router(email_controller)
app.include_router(category_controller)
app.include_router(news_controller)
app.include_router(document_type_controller)
app.include_router(biblioteca_controller)
app.include_router(location_controller)
app.include_router(culture_controller)
app.include_router(presidente_controller)
app.include_router(rol_controller)
app.include_router(multimedia_controller)
app.include_router(multimedia_historia_controller)
app.include_router(multimedia_cultura_controller)
app.include_router(categoria_historia_controller)
app.include_router(historia_controller)
app.include_router(routerfile)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
