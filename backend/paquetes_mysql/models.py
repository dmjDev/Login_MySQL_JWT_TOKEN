from sqlalchemy import Column, String, Integer, Boolean
from paquetes_mysql.database import Base

class ModelUser(Base):
    '''
    Docstring for ModelUser
    Este tipo de clases definen que elementos se deben crear si no lo están ya en la base de datos al iniciar la aplicación para evitar errores de base de datos
    Esto se realiza tras crear la conexión a la base de datos mediante "engine", el registro de metadatos mediante "Base"
    y ejecutando la sentencia "Base.metadata.create_all(bind=engine)"
    También se utiliza para generar nuevos registros, en este caso, nuevos usuarios pasando a sqlAlchemy los datos según esta estructura de datos
    '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True, unique=True, nullable=False)
    full_name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    disabled = Column(Boolean, index=True, default=True)
    hashed_password = Column(String(255), index=True, nullable=False)
