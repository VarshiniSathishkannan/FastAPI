from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from sqlalchemy import insert,select
from .routers import user,auth, post
from .config import settings

# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"])



models.Base.metadata.create_all(bind=engine)

while(True):
    try:
        connection = psycopg2.connect(database="fastapi_backend", user="postgres", password="123", host="localhost", port=5432, cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        # cursor.execute("SELECT * from posts;")
        # record = cursor.fetchall()
        # print("Data from Database:- ", record)
        print('DB connection was successful')
        break
    except Exception as error:
        print('Connection to DB failed',error)
        time.sleep(60)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)

# my_posts = [{"id":0,"title":"my family","content":"we are 4","rating":4},{"id":1,"title":"my friends","content":"close friends","rating":4}]

# Route/path operations

@app.get('/') 
# @ Decorator 
# get is http method, there are many methods which we can use.
async def root(): 
    # async for asynchronous functions, like database read or api call, optionaal. 
    # Function name can be anything.
    return {'message':'Hello World, I have made changes, again'} # JSON will be returned 

# @app.get('/posts')
# def get_posts():
#     cursor.execute('select * from posts;')
#     data = cursor.fetchall()
#     return {'data':data}

# # if we have multiple same path, it will return the first match in order

# @app.post('/createposts')
# def createPosts(payload: dict=Body(...)):
#     print(payload)
#     return {'message': f"title {payload['title']} and content {payload['content']}"}

# # Painpoints

# # Its a pain to get all the values from the Body. 
# # The client can send whatever data they want. 
# # Data isn't getting validated

# # We ultimately want to force the client to send data in a schema that we expect
# # For that purpose, we will be using pydantic

# # class Post(BaseModel):
# #     title:str
# #     content:str
# #     # rating:int
# #     publish:bool=True  # Default value is True,Optional (User may or may not send)
# #     # comment:Optional[str]=None

# @app.post('/posts',status_code=status.HTTP_201_CREATED)
# def createPostss(payload:schemas.Post):
#     # payload = payload.model_dump()
#     cursor.execute("""insert into posts (title,content,publish) values (%s,%s,%s) returning *""",(payload.title,payload.content,payload.publish)) # If we use f string here, it is susceptible to SQL injection 
#     post = cursor.fetchone()
#     connection.commit()
#     # payload['id']=len(my_posts)
#     # my_posts.append(payload)
#     # return {'message': f"title {payload.title} and content {payload.content} and rating {payload.rating}"}   
#     return {'data':post} 

# # CRUD

# # Create -- post  /posts
# # Read -- get     /posts (all) and /posts/:id (specific)
# # Update -- put/patch   /posts/:id
# # Delete -- delete /posts/:id

# # Naming should be plural (Best practices)

# # @app.get('/posts/latest')
# # def get_latest_post():
# #     return {"data":my_posts[-1]}

# @app.get('/posts/{id}') # path parameter {}
# def get_post(id:int,response:Response):
#     # print(id) #id is str, we need to define in function paramter
#     # if(id >= len(my_posts)):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID-{id} not found")
#     #     response.status_code = 404 # or
#     #     # response.status_code = status.HTTP_404_NOT_FOUND
#     #     return {"message":f"Post with ID-{id} not found"}
#     # else:
#     #     return {"data":my_posts[id]}
#     cursor.execute("""select * from posts where id = %s""",(str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id not found')
#     return {"data":post}
    
# # Below code results in error as it takes the above get request and expects a int
# # we need to order it correctly, so below code should go above

# # @app.get('/posts/latest')
# # def get_latest_post():
# #     return {"data":my_posts[-1]}

# @app.put('/posts/{id}')
# def update_post(id:int,payload:schemas.Post):
#     cursor.execute("""update posts set title = %s,content = %s,publish = %s where id = %s returning *""",(payload.title,payload.content,payload.publish,id))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not found")
#     connection.commit()
#     # if(id >= len(my_posts)):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not found")
#     # else:
#     #     payload = payload.model_dump()
#     #     my_posts[id]=payload  
#     return {'data':post} 
    
# @app.delete('/posts/{id}')
# def delete_post(id:int):
#     cursor.execute("""delete from posts where id = %s returning *""",(str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id not found')
#     # if(id >= len(my_posts)):
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id not found')
#     # else:
#     #     my_posts.pop(id)
#     connection.commit()
#     return {"data":post}

# # # Using SQLALCHEMY

# # @app.get('/sqlalchemy')
# # def test(db: Session = Depends(get_db)):
# #     posts = db.query(models.Post).all()
# #     return {"data":posts}

# # @app.post('/sqlalchemy',status_code=status.HTTP_201_CREATED)
# # def test(payload:schemas.Post,db: Session = Depends(get_db)):
# #     payload = payload.model_dump()
# #     # post = models.Post(title=payload.title,content=payload.content,publish=payload.publish) 
# #     # what if we have 50 columns ? instead of this approach, we can convert the payload into dictionary and unpack it
# #     post = models.Post(**payload)
# #     db.add(post)
# #     db.commit()
# #     db.refresh(post)
# #     return {'data':post}

# # @app.get('/sqlalchemy/{id}')
# # def test(id:int,db: Session = Depends(get_db)):
# #     post = db.query(models.Post).filter(models.Post.id==id).all() # all() will try to search all the records. if we are sure only 1 record is having that id we can give first()
# #     return {"data":post}

# # @app.delete('/sqlalchemy/{id}')
# # def test(id:int,db: Session = Depends(get_db)):
# #     post = db.query(models.Post).filter(models.Post.id==id)
# #     post.delete(synchronize_session=False)
# #     db.commit()
# #     return {"data":"success"}

# # @app.put('/sqlalchemy/{id}')
# # def test(id:int,payload:schemas.Post,db: Session = Depends(get_db)):
# #     post = db.query(models.Post).filter(models.Post.id==id)
# #     if(post.first() == None):
# #         return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Id is not found')
# #     payload = payload.model_dump()
# #     post.update(payload,synchronize_session=False)
# #     db.commit()
# #     return {"data":post.first()}

# # pydantic model for response, In return, no need to send data, FastAPI automatically serialises and sends the data. By default pydantic model expects a dict

# @app.get('/response/{id}',response_model=schemas.PostResponse)
# def test(id:int,db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id==id).first() # all() will try to search all the records. if we are sure only 1 record is having that id we can give first()
#     print(post)
#     return post

# # 'msg': 'Input should be a valid dictionary or object to extract fields from', 'input': [<app.models.Post object at 0x0000020AD5EA2CE0>]}

# @app.get('/response/',response_model=List[schemas.PostResponse])
# def test(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all() # all() will try to search all the records. if we are sure only 1 record is having that id we can give first()
#     print(post)
#     return post


    