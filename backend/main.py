from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  #CORS

from routes.app_routes import app_routes
from routes.user_routes import user_routes

# iniciamos la conexión a la base de datos / creación de la estructura básica si no existe con models.py
from paquetes_mysql import database
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(app_routes)
app.include_router(user_routes)

#ORIGENES PERMITIDOS FRONTEND #############################
origin = [
    ##LOCAL##
    'http://localhost:3000' # damos acceso a nuestro BackEnd únicamente desde esta URL FrontEnd local
    ##DOCKER##
    #'http://172.18.0.4:3000' # UNA VEZ LOS TRES CONTENEDORES CONECTADOS DESDE NUESTRA RED DOCKER SE ASIGNA A NUESTRO BACKEND LA IP DE NUESTRO FORNTEND
    #'*' # PARA DARA ACCESO ACUALQUIR IP PUBLICA
]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
###########################################################
