from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # Importamos OAuth2PasswordRequestForm. Clases fastAPI para el tratamiento de los datos de autenticación provenientes desde el formulario FrontEnd
from datetime import timedelta

from schemas.user import User, UserExtend, UserId, UserFull
from paquetes import user_management

from paquetes_mysql.database import get_db
from sqlalchemy.orm import Session

user_routes = APIRouter()

###################################################################################
# RUTAS DE USER_ROUTES PARA LA GESTIÓN DE DATOS DE USUARIOS
@user_routes.post('/app/users/', response_model=UserExtend, tags=["User data"])
def create_user(user: UserExtend, db: Session = Depends(get_db)):
    '''
    Docstring for create_user

    :param user: Diccionario con schema UserExtend, con los datos de usuario obtenidos desde el formulario del FrontEnd
    :type user: UserExtend
    :param db: Hace una petición de dependecia a GET_DB que crea una nueva sesión ORM con todos los parámetros preconfigurados en database.py
    :type db: Session
    GET_DB se detiene en YIELD
    :return: si el nombre de usuario no existe según GET_USER_BY_USERNAME y no se produce ninguna excepción, devuelve los datos del nuevo usuario
    siguiendo el modelo de datos ModelUser que devuelve CREATE_USER con el schema USEREXTEND cuyos parámetros son la sesión ORM obtenida 
    con GET_DB y los datos de usuario a almacenar en la base de datos
    GET_DB continúa tras el YIELD con FINALLY
    '''
    check_username = user_management.get_user_by_username(db=db, username=user.username)
    if check_username:
        raise HTTPException(status_code=400, detail="User already exists")
    return user_management.create_user(db=db, user=user)

# este UserId se puede modificar por cualquier tipo de schema para obtener el formato que queramos User, UserPass, UserExtend y UserId
@user_routes.get('/app/users/', response_model=list[UserId], tags=["User data"])
def get_users(db: Session = Depends(get_db)):
    '''
    Docstring for get_users

    :param db: Hace una petición de dependecia a GET_DB que crea una nueva sesión ORM con todos los parámetros preconfigurados en database.py
    :type db: Session
    GET_DB se detiene en YIELD
    :return: obtiene una lista de usuarios siguiendo el modelo ModelUser de GET_USERS con el schema USER, USERPASS, USEREXTEND o USERID 
    pasándo como parámetro la sesión ORM obtenida con GET_DB
    GET_DB continúa tras el YIELD con FINALLY
    '''
    return user_management.get_users(db=db)

# este UserId se puede modificar por cualquier tipo de schema para obtener el formato que queramos User, UserPass, UserExtend y UserId
@user_routes.get('/app/users/{id:int}', response_model=UserId, tags=["User data"])
def get_user(id: int, db: Session = Depends(get_db)):
    '''
    Docstring for get_user

    :param id: Recoge el dato ID del formulario de consulta desde el FrontEnd o desde cualquier otra función, instancia o método de clase
    :param db: Hace una petición de dependecia a GET_DB que crea una nueva sesión ORM con todos los parámetros preconfigurados en database.py
    :type db: Session
    GET_DB se detiene en YIELD
    :return: si el usuario existe y no ha sucedido ninguna excepción, obtiene los datos del usuario ID
    siguiendo el modelo ModelUser que devuelve GET_USER_BY_ID con el schema USERID y pasándo como parámetros la sesión ORM obtenida con GET_DB y el ID de usuario
    GET_DB continúa tras el YIELD con FINALLY
    '''
    user_by_id = user_management.get_user_by_id(db=db, id=id)
    if user_by_id:
        return user_by_id
    raise HTTPException(status_code=404, detail="User not found")
@user_routes.get('/app/users/UserFull/{id:int}', response_model=UserFull, tags=["User data"])
def get_user(id: int, db: Session = Depends(get_db)):
    user_by_id = user_management.get_user_by_id(db=db, id=id)
    if user_by_id:
        return user_by_id
    raise HTTPException(status_code=404, detail="User not found")

@user_routes.put('/app/users/{id:int}', response_model=User, tags=["User data"])
def update_user(id: int, updatedPost: User, db: Session = Depends(get_db)):
    updated_user = user_management.update_user_by_id(db=db, id=id, updatedPost=updatedPost)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not updated")

@user_routes.delete('/app/users/{id:int}', response_model=str, tags=["User data"])
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_msg = user_management.delete_user_by_id(db=db, id=id)
    if delete_msg:
        return delete_msg
    raise HTTPException(status_code=404, detail="User not deleted")

###################################################################################
# RUTAS DE USER_ROUTES PARA LA AUTENTICACIÓN
@user_routes.get("/users/on", response_model=User, tags=["User login"])
def user(user: User = Depends(user_management.get_user_current)):
    '''
    1.Docstring for user

    :param user: Resultado de ejecutar la función dependiente GET_USER_DISABLED_CURRENT donde se evalua si el usuario se encuentra activo o no
    :type user: User
    :return: objeto Schema de datos USER con los datos del usuario autenticado
    Podemos mostrar cualquiera de los 4 schemas de usuario, para ello habría que modificar el valor en la llamada a esta función y
    en la función GET_CURRENT_USER de user_management.py, en el apartado RECUPERACION DE LOS DATOS DE USUARIO.
    '''
    return user

@user_routes.post("/token", response_model=dict, tags=["User login"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    3.Docstring for login

    :param form_data: Recoge los datos del formulario de autenticación desde el FrontEnd
    :type form_data: OAuth2PasswordRequestForm
    :AUTHENTICATE_USER: Función que recibe el username y password del formulario FrontEnd, obteniendo como resultado si los datos de usuarios 
    son correctos, los valores de este usuario como un objeto USERPASS, ACCESS_TOKEN_EXPIRES nos servirá para establecer cuanto tiempo debe 
    de existir el token
    :return: Devuelve un diccionario con dos valores ACCESS_TOKEN y TOKEN_TYPE que se pasa a la función GET_USER_CURRENT de user_management.py
    '''
    user = user_management.authenticate_user(form_data.username, form_data.password)                # 4.1
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = user_management.create_token({"sub": user.username}, access_token_expires)   # 4.2
    print("access", access_token_jwt)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

