from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from src.database import Base, metadata


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {'extend_existing': True}

    id= Column(Integer,primary_key=True)
    name= Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('role.id'))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


    @property
    def posts(self):
        from src.posts.models import Posts
        return relationship("Posts", back_populates="user")
