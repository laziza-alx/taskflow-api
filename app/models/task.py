from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base 

class Task(Base): 
    __tablename__ = "tasks"
# это для того чтобы ид был уникальным и индексированным
    id = Column(Integer, primary_key = True, index = True)
    # название задачиб не может быть пустым 
    title = Column(String(100), nullable = False)
    #  описание задачи можем быть пустым 
    description = Column(Text, nullable = True)
    #  статус задачи по умолчанию "pending"
    status = Column(String(20), default = "pending", nullable = False)
    
# это свящь с таблицей пользователей
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
#  создает орм и связь между объектами
    user = relationship("User", back_populates="tasks")