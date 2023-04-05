import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_model import Base


class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    url_font = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("UserModel",
                           back_populates="articles",
                           lazy="joined")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

