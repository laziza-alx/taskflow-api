import os
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from jose import jwt

#читает переменные окружения из файла .env
load_dotenv()

# берет значения переменных окружения из файла .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# создaет токен доступа на основе данных, переданных в виде словаря  
def create_access_token(data: dict):
    # копирует данные, чтобы не изменять исходный словарь
    to_encode = data.copy()
    
    # устанавливает время истечения токена на 30 минут от текушего времени
    expire = datetime.now(UTC)+ timedelta(minutes = 30)
    # добавляет время истечения токена в словарь данных 
    to_encode.update({"exp": expire})
    
    # берет секретный ключ и алгоритм из перменных окр и создает токен доступа с библиотекой jose
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )    
    return encoded_jwt

