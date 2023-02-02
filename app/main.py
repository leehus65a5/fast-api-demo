from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import get_db, engine, Base
from sqlalchemy.orm import Session
from api import user, curve_value
from schemas import User_base
from typing import Any

app = FastAPI()

app.include_router(user.routes)
app.include_router(curve_value.routes)


class Post(BaseModel):
     title: str
     body: str
     id : int
     public: bool = True
     rating: Optional[int] = None

mypost = [{"title":"title 1111", "body":"body 111","id":1},
          {"title":"title 222", "body":"body 222","id":2}]

# @app.on_event("startup")
# async def startup():
#      # await get_db().connect()
#      # from models import User
#      base.metadata.create_all(engine)
# #     metadata.create_all(engine)



# @app.on_event("shutdown")
# async def shutdown():
#     await get_db().disconnect()

@app.get("/", response_model = list[User_base])
async def root(db: Session = Depends(get_db)) -> Any:
     from models import User
     x = db.query(User).all()
     print('type of x = ', type(x))
     for i in x:
          print(i.user_id, i.user_name, i.password, i.role)
     if x: 
          return x
     return {"message": "my first api"}

@app.get("/posts")
async def posts():
	return {"message": mypost}

@app.post("/create")
async def create_content(post: Post):
     print(post.dict())
     mypost.append(post.dict())
     return {"message": f"content : {mypost}"}

@app.get("/post/{id}")
async def get_post_id(id:int, response: Response):
     post = None
     for p in mypost:
          if p.get("id") == id:
               post = p
               
     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id {id} not found")
     
     print('respone = ', response)
     return {"post detail": post}