import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.orm import relationship

from app.db.base_model import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_complete = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telephone = Column(String(15), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)

    # orphan é para não deixar artigos sem usuário, não deixar eles sem "pais" ou "orfãos"
    articles = relationship("ArticleModel",
                            cascade="all, delete-orphan",
                            back_populates="creator",
                            uselist=True,
                            lazy="joined")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
