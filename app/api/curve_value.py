from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Curve_value
from database import get_db
from schemas import Curve_value_out, User_base
from typing import Any
from api.auth import login_user

routes = APIRouter(prefix='/curve-value', tags=['curve-value'])

@routes.get('/all', response_model=list[Curve_value_out])
async def get_all_curve_value(db: Session = Depends(get_db)) -> Any:
    """Lấy ra toàn bộ bảng dữ liệu cal_curve_valu

    Args:
        db (Session, optional): Gọi database.
         Defaults to Depends(get_db).
    Returns:
        Trả về danh sách các dòng có kiểu dữ liệu định dạng theo 
        Curve_value_out schemas
    """
    get_curve_value = db.query(Curve_value).all()
    return get_curve_value

@routes.get('/{well_id}', response_model=list[Curve_value_out])
async def get_all_curve_value(well_id: str, db: Session = Depends(get_db)) -> Any:
    """Lấy ra bảng dữ liệu well-log theo well_id từ bảng dữ lieju cal_curve_value

    Args:
        well_id (str): tên của bảng dữ liệu, kiểu dữ liệu là str
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        Trả về danh sách các dòng có kiểu dữ liệu định dạng theo 
        Curve_value_out schemas
    """
    get_curve_value_by_id = db.query(Curve_value).filter(
        Curve_value.well_id == well_id).all()

    if not get_curve_value_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"well_id {well_id} not found")

    return get_curve_value_by_id
