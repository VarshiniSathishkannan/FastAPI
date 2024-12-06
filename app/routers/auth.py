from .. import models,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import engine,get_db
from sqlalchemy.orm import Session
from ..oauth2 import create_access_token

router = APIRouter(prefix='/login',tags=['Auth'])

# @router.post('/')
# def get_user(payload:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
#     # OAuth2PasswordRequestForm will return username and password
#     email = payload.username
#     user = db.query(models.User).filter(models.User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
#     if not (utils.verify(payload.password,user.password)):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
#     access_token = create_access_token({"user_id":user.id})
#     return {"access_token":access_token,"token_type":"bearer"}

# For above we need to give data in form-data instead of raw with key and value as username and password

@router.post('/',response_model=schemas.Token)
def get_user(payload:schemas.User,db: Session = Depends(get_db)):
    email = payload.email
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    if not (utils.verify(payload.password,user.password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    access_token = create_access_token({"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}

