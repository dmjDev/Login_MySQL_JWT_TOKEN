from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    # Genera un nuevo hash con un salt aleatorio y el costo por defecto (12)
    return pwd_context.hash(password)

print(hash_password("clave"))