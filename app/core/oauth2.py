
# фастапи сам достанет ЖВТ токен из запроса  и если неверный токен то вернем ошибку
from fastapi import Depends, HTTPException
# читает токен из жвт и проверяет его
from fastapi.security import OAuth2PasswordBearer
# надо дляработы базы данных чтобы получить пользователя по токену 
from sqlalchemy.orm import Session
# библиотека для работы с жвт токенами создавать проверять и расшифровывать
from jose import JWTError, jwt

# чтобы получить соединение с бд 
from app.database.dependencies import get_db
from app.database.connection import SessionLocal
# чтобы искать пользователя по токену и получить его данные 
from app.models.user import User
#используем тот самый ключ и алгоритм чтобы проверить токен и расшифровать его
from app.core.jwt import SECRET_KEY, ALGORITHM

# создает экземпляр котрыц будет проверять токен в запросе и если токен неверный то вернет ошибку 401
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/users/login"
)
# функция которая будет получать текщего
def get_current_user(
    # автоматически передаст
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    try:
        # расшифровает токен и получает данные из него 
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # получаем эмаил усера из токена
        email = payload.get("sub")
        
        
        if email is None:
            raise HTTPException(
                status_code = 401,
                detail= "invalid token"
            )
     # если токен поврежден или поддкльный то библиотека вызовет        
    except JWTError:
        raise HTTPException(
            status_code = 401,
            detail= "invalid token" 
        )
        
    # по эмаил ищем пользователя     
    user = db.query(User).filter(
        User.email == email
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
