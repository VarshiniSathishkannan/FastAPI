from .. import models,schemas,utils,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix='/vote',tags=['Votes'])

@router.post('/')
def test(payload:schemas.Vote,db: Session = Depends(get_db),user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()  
    if(not post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Given PostID not found")
    if(payload.dir):
        vote = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id,models.Vote.user_id == user.id).first()
        if not vote:
            new_vote = models.Vote(user_id=user.id,post_id = payload.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {'data':"success"}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="User has already voted on this post")
    else:
        vote = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id,models.Vote.user_id == user.id)
        if not vote.first():
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="User has not liked this post")
        else:
            vote.delete(synchronize_session=False)
            db.commit()
            return {'data':'success'}
            
        
    