import secrets
import string

def generate_secure_key(length=32):
    # Определяем набор символов, включая буквы, цифры и специальные символы
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secure_key

jwt_secret_key = generate_secure_key(32)
