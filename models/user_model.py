from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50), index=True)
    lastName = Column(String(50), index=True)
    email = Column(String(120), index=True)
    password = Column(String)
    role = Column(String(50), index=True)
    isActive = Column(Boolean, index=True)
    
    def to_dict(self, exclude=None):
        exclude = exclude or []
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and key not in exclude}