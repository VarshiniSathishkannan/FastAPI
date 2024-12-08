from pydantic import BaseModel,ConfigDict, EmailStr
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    # rating:int
    publish:bool=True  # Default value is True,Optional (User may or may not send)
    # comment:Optional[str]=None
    
class CreatePost(BaseModel):
    title:str
    content:str
    publish:bool=True  
    
class UpdatePost(BaseModel):
    title:str
    content:str
    publish:bool=True 
    
# Or we can create a base post and extend it

class BasePost(BaseModel):
    title:str
    content:str
    publish:bool=True 

class CreatePost2(BasePost):
    pass

class UpdatePost2(BasePost):
    pass



class User(BaseModel):
    email:EmailStr
    password:str
    
class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title:str
    content:str
    publish:bool
    owner:User
    
class UserOut(BaseModel):
    email:EmailStr

class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
    
class Vote(BaseModel):
    post_id:int
    dir:bool