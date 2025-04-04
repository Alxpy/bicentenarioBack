import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.controllers.user_controller import user_controller
from src.presentation.controllers.auth_controller import auth_controller
from src.presentation.controllers.email_controller import email_controller
from src.presentation.controllers.token_controller import token_controller
from src.presentation.controllers.routes_controller import routes_controller
from src.presentation.controllers.categoriaNoticia_controller import categoriaNoticia_controller
from src.presentation.controllers.noticia_controller import noticia_controller
from src.presentation.controllers.tipoDocumento_controller import tipoDocumento_controller
from src.presentation.controllers.biblioteca_controller import biblioteca_controller


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller)
app.include_router(auth_controller)
app.include_router(email_controller)
app.include_router(token_controller)
app.include_router(routes_controller)
app.include_router(categoriaNoticia_controller)
app.include_router(noticia_controller)
app.include_router(tipoDocumento_controller)
app.include_router(biblioteca_controller)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
