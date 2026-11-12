from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    hash_password,
    verify_password 
)

from app.core.oauth2 import get_current_user

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate


from app.schemas.user import UserLogin

from app.core.jwt import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Создать пользователя
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    return new_user


# Получить всех пользователей
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Получить пользователя по ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# Обновить пользователя
@router.put("/{user_id}", response_model = UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id ==user_id ).first()
    
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.username = user_data.username
    user.email = user_data.email

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return user

# Удалить пользователя 
@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail = "User not found"
        )
        
    db.delete(user)
    db.commit()
    
    return{
        "message": "User deleted successfully"
    }
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        
    # создание токена доступа с помощью  функции
    access_token = create_access_token(
        # в качестве данных для токена передаем емаил пользователя в виде словаря 
        data = {"sub": db_user.email}
        )

    # возвращаем токен доступа и тип токена в виде словаря
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
# создает новый маршрут GET/USER/ME   
@router.get("/me", response_model= UserResponse)
def get_me(
    # в функцию уже приходит готовый объеки пользователя 
    current_user: User = Depends(get_current_user)
):
    return current_user