import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from dotenv import load_dotenv
load_dotenv()
##LOCAL##
##Parámetros de conexión de forma local con un BackEnd en un entorno virtual (revisar .env)
DB_HOST = os.getenv('DB_HOST', default=None)
DB_PORT_LOCAL = os.getenv('DB_PORT_LOCAL', default=None)  # COMENTAMOS ESTA LÍNEA AL CONECTAR MEDIANTE LOS CONTENEDORES
DB_USER = os.getenv('DB_USER', default=None)
DB_PASSWORD = os.getenv('DB_PASSWORD', default=None)
DB_NAME = os.getenv('DB_NAME', default=None)
DB_DIALECT = os.getenv('DB_DIALECT', default=None)
DATABASE_URL = (
    f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT_LOCAL}/{DB_NAME}"
)

##DOCKER##
# Parámetros de conexión con contenedor BackEnd (revisar .env)
# DB_HOST = os.getenv('DB_HOST', default=None)
# DB_USER = os.getenv('DB_USER', default=None)
# DB_PASSWORD = os.getenv('DB_PASSWORD', default=None)
# DB_NAME = os.getenv('DB_NAME', default=None)
# DB_DIALECT = os.getenv('DB_DIALECT', default=None)
# DATABASE_URL = (
#     f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# )

# Intentar crear el motor de SQLAlchemy "engine" con reintentos - CONEXIÓN A LA BASE DE DATOS
max_retries = 5
engine = None

for attempt in range(max_retries):
    try:
        # Crea el motor de la base de datos
        # echo=True mostrará las consultas SQL generadas por SQLAlchemy en la consola (útil para depurar)
        engine = create_engine(DATABASE_URL, echo=True)
        
        # Intentar conectar inmediatamente para verificar que funciona
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos MySQL usando SQLAlchemy.")
            # Opcional: ejecutar una consulta simple para probar
            result = connection.execute(text("SELECT 1"))
            print(f"Resultado de la prueba: {result.scalar()}")
        break
    
    except Exception as e:
        if attempt < max_retries - 1:
            print(f"Error de conexión: {e}. Reintentando en 5 segundos... (Intento {attempt + 1}/{max_retries})")
            time.sleep(5)
        else:
            print(f"Error de conexión persistente. No se pudo conectar a la base de datos.")
            raise

# A partir de aquí puedes usar 'engine' para todas tus operaciones de SQLAlchemy
# Por ejemplo, para crear sesiones ORM o ejecutar más consultas.

# CREA UNA SESION ORM
# ORM(Object Relational Mapping) nos permite interactuar con la base de datos relacional sin tener que crear consultas SQL 
# Mediante el mapeo de intrucciones simples que se convierten en consultas SQL, ej. usuario.guardar() --> INSERT INTO usuarios.....
localSession = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
# "Base" crea el registro de metadatos capaces de mapear las consultas sqlalchemy hacia la base de datos relacional transformándolas en consultas SQL
Base = declarative_base()

def get_db():
    '''
    Docstring for get_db
    
    YIELD: retorna la variable DB donde se crea una sesión ORM con todos los parámetros preconfigurados en database.py
    Esta función va a ser invocada mediante DEPENDS por otras funciones, se trata de una función dependiente,
    de este modo se ejecutará siguiendo el siguiente esquema:
    - Ejecuta GET_DB hasta YIELD
    - Ejecuta la función principal hasta un return o un raise
    - Ejecuta GET_DB desde YIELD
    '''
    db = localSession()
    try:
        yield db
    finally:
        db.close
