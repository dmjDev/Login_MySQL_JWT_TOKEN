from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional  # Importamos OPTIONAL para asignar dicha propiedad a los campos que tienen valor por defecto o diferentes posibilidades de tipos de datos

# SCHEMA DE DATOS
class User(BaseModel):
    '''
    Docstring for User
    Esquema de datos con los datos básicos de usuario
    '''
    # ConfigDict(orm_mode=True) en Pydantic v1
    # biblioteca Pydantic que dota a los tipos de datos SCHEMA(User, UserPass y UserId) de la función MODEL_VALIDATE para crear objetos de tipo
    # SCHEMA(diccionario) a partir de datos de tipo MODEL como lo son los de datos SQLAlchemy u ORM resultado de una consulta de base de datos
    # schema_data = SCHEMA.model_validate(model_data)
    # models_data --> dato de tipo Model, como por ejemplo de SQLAlchemy u ORM 
    # schema_data --> dato de tipo Schema como diccionario formado a partir de un dato tipo Model
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    email: str
    disabled: bool = True
    
class UserId(User):
    id: int
    
class UserPass(User):
    hashed_password: str
    
class UserLogin():
    ultimo_login: date
    
class UserExtend(UserPass, UserLogin):
    fecha_registro: date
    rol: int = 0
    
class UserFull(UserExtend):
    id: int