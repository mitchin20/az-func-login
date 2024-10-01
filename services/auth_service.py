from sqlalchemy.orm import Session
from models.user_model import User
from services.verify_password import verify_password

# Authentication user
def authentication_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return None
    
    return user.to_dict(exclude=["password"])

# Handle login logic
def login_user(db: Session, email: str, password: str):
    user_info = authentication_user(db, email, password)
    
    return user_info