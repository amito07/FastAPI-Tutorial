from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_function(data):
    return pwd_context.hash(data)

def verify_hash_function(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

