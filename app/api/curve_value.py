from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Curve_value
from database import get_db
from schemas import Curve_value_out
from typing import Any

routes = APIRouter(prefix='/curve-value', tags=['curve-value'])

@routes.get('/all', response_model= list[Curve_value_out])
async def get_all_curve_value(db: Session = Depends(get_db)) -> Any:
     get_curve_value = db.query(Curve_value).all()
     return get_curve_value
     
@routes.get('/{well_id}', response_model= list[Curve_value_out])
async def get_all_curve_value(well_id : str, db: Session = Depends(get_db)) -> Any:
     
     get_curve_value_by_id = db.query(Curve_value).filter(Curve_value.well_id == well_id).all()
     
     if not get_curve_value_by_id:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"well_id {well_id} not found")
          
     return get_curve_value_by_id


# @routes.get('/')
# async def get_well_by_curve():
     
#      pass