from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Secret key
# algorithm
# expiration time

SECRET_KEY = "80897979r00232070uu0hijb0320703707302h"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def validate_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        # token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return id
    
def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token = validate_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token).first()
    return user