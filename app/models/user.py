from sqlalchemy import Column, String, DateTime, Boolean
from app.models.base import BaseModel
from sqlalchemy.sql import func
import uuid


class User(BaseModel):
    # 指定数据库表名称
    __tablename__ = "user"

    id = Column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:32])
    #
    username = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(128), nullable=True, unique=True, index=True)
    password_hash = Column(
        String(255),
        nullable=True,
    )
    email = Column(String(128), nullable=True, unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self, include_password=False, **kwargs):
        exclude = ["password_hash"] if not include_password else []
        return super().to_dict(exclude=exclude, **kwargs)
