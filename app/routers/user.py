from .. import models,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users',tags=['Users'])

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def test(payload:schemas.User,db: Session = Depends(get_db)):
    payload = payload.model_dump()
    # post = models.Post(title=payload.title,content=payload.content,publish=payload.publish) 
    # what if we have 50 columns ? instead of this approach, we can convert the payload into dictionary and unpack it
    hashed_password = utils.hash(payload['password'])
    payload['password']=hashed_password
    user = models.User(**payload)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id is not found')
    return user