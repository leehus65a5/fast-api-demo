from .auth import login_user
from models import User, Per_mission
from schemas import User_base
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
from enum import Enum, unique


@unique
class PER(Enum):
    READ = "read_per"
    WRITE = "write_per"
    DELETE = "delete_per"


routes = APIRouter(prefix='/permission', tags=['permission'])


class RoleChecker:
    def __init__(self, allowed_roles: list) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(login_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'User: {user.user_name} do not have role to access this api')


allow_admin_roles = RoleChecker(['admin'])
allow_datamanager_roles = RoleChecker(['data', 'admin'])
allow_reviewer_roles = RoleChecker(['review', 'data', 'admin'])


class PerMission:
    def __init__(self, allow_permission: Enum, table) -> None:
        self.allow_permission = allow_permission
        self.table = table

    def __call__(self, user: User = Depends(login_user), db: Session = Depends(get_db)):
        uid = user.user_id
        get_per = db.query(Per_mission).filter(
            and_(Per_mission.user_id == uid, Per_mission.tb_name == self.table)).first()
        if not get_per or not getattr(get_per, self.allow_permission.value):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"User {user.user_name} do not permission to this api")


@routes.get('/admin/getuser', response_model=list[User_base], dependencies=[Depends(allow_admin_roles)])
async def get_user_by_admin(db: Session = Depends(get_db)):
    """get all user by admin roles permission
    Args:
        db (Session, optional): Defaults to Depends(get_db).
        - Lấy ra database manager
    Returns:
        User_base : Trả về danh sách người dùng theo User_base shemmas
    """
    all_user = db.query(User).all()
    return all_user


@routes.get('/test', dependencies=[Depends(PerMission(PER.READ, 'A10')), Depends(allow_admin_roles)])
async def test_per():
    return 'check'
