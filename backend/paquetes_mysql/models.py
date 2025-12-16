from sqlalchemy import Column, String, Integer, Boolean, Date
from paquetes_mysql.database import Base

# MODELO ORM PARA SQLALCHEMY
class ModelUser(Base):
    '''
    Docstring for ModelUser
    
    Creación de la estructura inicial de la base de datos --> Base.metadata.create_all(bind=engine)
    También se utiliza para generar nuevas Operaciones SQLAlchemy ORM (Insert, Select/Filter, Update, Delete)
    '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True, unique=True, nullable=False)
    nombre_completo = Column(String(255), index=True)
    fecha_nacimiento = Column(Date, index=True)
    email = Column(String(255), index=True)
    disabled = Column(Boolean, index=True, default=True)
    hashed_password = Column(String(60), index=True, nullable=False)
    fecha_registro = Column(Date, index=True)
    ultimo_login = Column(Date, index=True)
    rol = Column(Integer, index=True, nullable=False)
