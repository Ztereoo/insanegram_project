from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON, LargeBinary, MetaData
from sqlalchemy.orm import relationship



from src.database import Base,metadata



class Posts(Base):
    __tablename__ = 'posts'
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    tags = Column(JSON, nullable=False)
    photo = Column(LargeBinary, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def user(self):
        from src.auth.models import User
        return relationship('User', back_populates="posts")