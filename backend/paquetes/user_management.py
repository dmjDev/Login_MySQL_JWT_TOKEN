'''
Funciones para la gestión de la tabla de datos "usuarios".
Funciones de manejo de datos de usuarios:
-get_db
-get_users
-get_user_by_id
-get_user_by_username
-create_user
Funciones de autenticación con token:
-verify_password
-authenticate_user
-create_token
-get_user_current
-get_user_disabled_current
'''
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer   # Importamos OAuth2PasswordBearer. Clases fastAPI para la creación del token de usuario una vez autenticado
from typing import Union                            # Importamos Union desde typing. Clase de tipo de datos que se utiliza para declarar atributos que puedan obtener diferentes tipos de datos
from passlib.context import CryptContext            # Importamos la clase CryptContext desde passlib que nos generará la codificación del password proveniente del FrontEnd para poder comparalo con el de la DB
from datetime import datetime, timedelta, UTC       # Necesitamos datetime y timedelta para asignar al token el lapso de tiempo que permanecerá activo
from jose import jwt, JWTError                      # Importamos la fuhnción jwt para codificar y decodificar el token y JWTError para manejar posibles excepciones en la decodificación

from paquetes_mysql.models import ModelUser
from schemas.user import User, UserPass, UserExtend

from paquetes_mysql.database import localSession
from sqlalchemy.orm import Session

from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', default=None)
ALGORITHM = os.getenv('ALGORITHM', default=None)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # Instancia de la clase CRYPTCONTEXT, cuyo método VERIFY va a comparar el password en texto plano pasado a través del formulario FrontEnd y el password encriptado obtenido de la base de datos

# FUNCIONES DE USER_MANAGEMENT PARA LA GESTIÓN DE DATOS DE USUARIOS
def create_user(db: Session, user: UserExtend):
    new_user = ModelUser(
        username = user.username,
        nombre_completo = user.nombre_completo,
        fecha_nacimiento = user.fecha_nacimiento,
        email = user.email,
        disabled = user.disabled,
        hashed_password = pwd_context.hash(user.hashed_password),
        fecha_registro = user.fecha_registro,
        ultimo_login = user.ultimo_login,
        rol = user.rol
    )
    db.add(new_user)
    db.commit()
    db.flush(new_user)
    return new_user

def get_users(db: Session):
    result = db.query(ModelUser).all()
    return result

def get_user_by_username(db: Session, username: str):
    result = db.query(ModelUser).filter(ModelUser.username == username).first()
    return result

def get_user_by_id(db: Session, id: int):
    result = db.query(ModelUser).filter(ModelUser.id == id).first()
    return result

def update_user_by_id(db: Session, id: int, updatedPost: User):
    result = db.query(ModelUser).get(id)
    if result:
        result.username = updatedPost.username
        result.nombre_completo = updatedPost.nombre_completo
        result.fecha_nacimiento = updatedPost.fecha_nacimiento
        result.email = updatedPost.email
        result.disabled = updatedPost.disabled
    db.commit()
    return result

# FUNCIONES DE USER_MANAGEMENT PARA LA AUTENTICACIÓN
def verify_password(plane_password, hashed_password):
    '''
    3.1.1.Docstring for verify_password
    
    :param plane_password: Password pasado desde el formulario FrontEnd
    :param hashed_password: Password encriptado proveniente de la base de datos
    :return: Encripta el pasword del formulario y lo compara con el de la base de datos y devuelve True o False
    '''
    return pwd_context.verify(plane_password, hashed_password)  

def authenticate_user(username: str, password: str):
    '''
    3.1.Docstring for authenticate_user
    
    :param username: String con el nombre de usuario pasado desde el formulario FrontEnd
    :param password: String con el password de usuario pasado desde el formulario FrontEnd
    :GET_USER_BY_USERNAME: devuelve un diccionario con los datos del usuario o una lista vacía
    :Condicional USER: En caso de devolver una lista vacía el condicional devuelve un raise con un mensaje de excepción 401
    y la cabecera para poder manejar el error desde el FrontEnd
    :Condicional VERIFY_PASSWORD: ejecuta la función VERIFY_PASSWORD pasándo como parámetros el password obtenido desde el formulario FrontEnd
    y el password encriptado obtenido de la base de datos, verifica que coincidan o no, obteniendo True o False
    :return: devuelve los datos en schema UserPass del usuario de tipo diccionario
    '''
    with localSession() as db:
        user_ModelUser = get_user_by_username(db, username)
        schemaUser = UserPass.model_validate(user_ModelUser) if user_ModelUser is not None else []
    
    if not schemaUser:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, schemaUser.hashed_password):
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return schemaUser

def create_token(data: dict, time_expire: Union[datetime, None]):
    '''
    3.2.Docstring for create_token
    
    :param data: Diccionario con el nombre de usuario {"sub": user.username}
    :type data: dict
    :param time_expire: Tiempo que el token va a existir antes de ser eliminado, timedelta
    :type time_expire: Union[datetime, None]
    :Condicional TIME_EXPIRE: Declaración de la variable expires, bien como parámetro recibido o bien como dato generado, que añadiremos al diccionario DATA_COPY
    :TOKEN_JWT: Codificamos el token en función de los datos pasados
    :return: devuelve la cadena de texto token_jwt
    '''
    data_copy = data.copy()
    if time_expire == None:
        expires = datetime.now(UTC) + timedelta(minutes=15)
    else:
        expires = datetime.now(UTC) + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

oauth2_scheme = OAuth2PasswordBearer("/token")
def get_user_current(token: str = Depends(oauth2_scheme)):
    '''
    2.Docstring for get_user_current
    
    OAUTH2_SCHEME: ejecuta la función dependiente LOGIN de la ruta /token antes de ejecutar GET_USER_CURRENT
    :param token: Diccionario con dos valores ACCESS_TOKEN y TOKEN_TYPE resultado de la función LOGIN en la ruta "/token"
    :type token: str
    :token_decode -> obtenemos el token decodificado
    :username: si decode funciona correctamente obtenemos el nombre de usuario
    :raise username None: excepción si el username no existe
    :raise except: si decode ha tenido alguna excepción
    :GET_USER_BY_USERNAME: si username existe en la base de datos obtenemos todos los datos de usuario con el formato de models MODELUSER
    :raise not user: si el username no existe en la base de datos
    :return: devuelve los datos de usuario según el Schema de datos User de tipo diccionario o una lista vacía
    '''
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    # RECUPERACION DE LOS DATOS DE USUARIO
    with localSession() as db:
        user_ModelUser = get_user_by_username(db, username)
        schemaUser = User.model_validate(user_ModelUser) if user_ModelUser is not None else []
    
    if not schemaUser:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    if schemaUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return schemaUser

