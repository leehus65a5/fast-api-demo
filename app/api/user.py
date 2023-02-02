from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import User_base, New_user, Update_user
from typing import Any

routes = APIRouter(prefix='/user', tags=['user'])

@routes.get('/all', response_model=list[User_base])
def get_all_user(db: Session = Depends(get_db)) -> Any:
     """lấy toàn bộ bảng dữ liệu user.

     Args:
         db (Session, optional): _description_. Defaults to Depends(get_db).

     Returns:
         Một danh sách người dùng trong bảng dữ liệu user.
     """
     all_user = db.query(User).all()
     return all_user

@routes.get('/{user_id}', response_model=User_base)
def get_user_by_id(user_id : str,db: Session = Depends(get_db)) -> Any:
     """Lấy thông tin người dùng theo ID

     Args:
         user_id (str): ID của người dùng được nhập trên URL. VD: VPI001
         db (Session, optional): _description_. Defaults to Depends(get_db).

     Raises:
         HTTPException: 404 nếu không tìm thấy người dùng theo id nhập vào.

     Returns:
         Any: Dữ liệu người dùng theo lược đồ User_base
     """
     
     get_user = db.query(User).filter(User.user_id == user_id).first()
     
     if not get_user:
          raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                              detail=f'the user id {user_id} not found')
          
     return get_user

@routes.post('/create', response_model=User_base)
async def create_new_user(new_user: New_user, db: Session = Depends(get_db)):
     """Tạo mới người dùng

     Args:
         new_user (New_user): Tạo mới người dùng theo request body json. 
          Xem thêm New_user shemas để lấy thông tin.
         db (Session, optional): _description_. Defaults to Depends(get_db).

     Raises:
         HTTPException: 404 Báo lỗi nếu người dùng mới nhập vào trùng username hoặc user_id
     

     Returns:
         _type_: trả về người dùng mới được nhập vào hệ thống, tuân theo chuẩn User_base shemas
     """
     user = User(**new_user.dict())
     check = db.add(user)
     try:
          db.commit()
     except:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail= f"error while insert name : {user.user_name}, id: {user.user_id}")
     
     return user

@routes.put('/{user_id}')
async def update_user(update_user: Update_user,user_id: str, db: Session = Depends(get_db)):
     """Update người dùng theo user_id

     Args:
         update_user (Update_user): Trường thông tin được dùng để update User, tuân theo chuẩn Update_user schemas
         user_id (str): id của người dùng cần update
         db (Session, optional): _description_. Defaults to Depends(get_db).

     Raises:
         HTTPException: 404 nếu người dùng không tồn tại hoặc xảy ra lỗi khi update.
     422: nếu validate dữ liệu không thỏa mãn.

     Returns:
         _type_: Trả về dữ liệu người dùng sau khi update tuân theo lược đồ Update_user 
     """
     query = db.query(User).filter(User.user_id == user_id).update(update_user.dict())
     
     if not query:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"the user id {user_id} not found")
     
     db.commit()
     return update_user

@routes.delete('/{user_id}')
async def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
     """Xóa người dùng theo ID

     Args:
         user_id (str): id của người dùng
         db (Session, optional): _description_. Defaults to Depends(get_db).

     Raises:
         HTTPException: 404 nếu user_id không tồn tại.
     """
     query = db.query(User).filter(User.user_id == user_id).delete()

     if not query:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"the user id {user_id} not found")
     db.commit()

