from pydantic import BaseModel, ConfigDict
'''Importamos Union desde typing. Clase de tipo de datos que se utiliza para declarar atributos que puedan obtener diferentes tipos de datos
Importamos Optional para asignar dicha propiedad a los campos que tienen valor por defecto o son autoincrement'''
from typing import Union, Optional

'''Schema de datos'''
class User(BaseModel):
    '''
    Docstring for User
    Esquema de datos con los datos básicos de usuario
    '''
    # ConfigDict(orm_mode=True) en Pydantic v1
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None
    
class UserPass(User):
    '''
    Docstring for UserPass
    Esquema de datos que recoge los datos básicos de usuario con "User" y le añade el password
    '''
    hashed_password: str
    
class UserId(UserPass):
    '''
    Docstring for UserId
    Esquema de datos que recoge los datos básicos de usuario con "User" y el password con "UserPass" y le añade el id de usuario
    '''
    id: Optional[int]=None