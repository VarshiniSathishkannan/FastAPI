from .. import models,schemas,utils,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix='/posts',tags=['Posts'])

@router.get('/')
def test(db: Session = Depends(get_db),limit:int=2,skip:int=0,search:Optional[str]=""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.content.contains(search)).all()
    return {"data":posts}

@router.post('/',status_code=status.HTTP_201_CREATED)
def test(payload:schemas.Post,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)):
    print(user.email)
    payload = payload.model_dump()
    payload['user_id'] = user.id
    # post = models.Post(title=payload.title,content=payload.content,publish=payload.publish) 
    # what if we have 50 columns ? instead of this approach, we can convert the payload into dictionary and unpack it
    post = models.Post(**payload)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {'data':post}

@router.get('/{id}',response_model=schemas.PostResponse)
def test(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first() # all() will try to search all the records. if we are sure only 1 record is having that id we can give first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post with given ID not found')
    print(post)
    return {"data":post}

@router.delete('/{id}')
def test(id:int,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post ID not found')
    if(post.first().user_id == user.id):
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Post does not belong to the user')
    return {"data":"success"}

@router.put('/{id}')
def test(id:int,payload:schemas.Post,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if(post.first() == None):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id is not found')
    payload = payload.model_dump()
    post.update(payload,synchronize_session=False)
    db.commit()
    return {"data":post.first()}