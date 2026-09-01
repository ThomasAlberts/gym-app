import bcrypt
import hashlib

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hashed password"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def hash_token(token: str) -> str:
    # refresh tokens zijn al random/lang genoeg; SHA-256 volstaat om ze niet
    # in plaintext in de db te bewaren
    return hashlib.sha256(token.encode()).hexdigest()