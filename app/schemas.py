from pydantic import BaseModel

#------------------USER SCHEMAS--------------#

class User_base(BaseModel):
    user_id: str
    user_name: str
    role: str

    class Config:
        orm_mode = True

class Update_user(BaseModel):
    user_name: str | None = None
    role: str | None = None
    
    class Config:
        orm_mode = True
        
class New_user(BaseModel):
    user_id: str
    user_name: str
    password: str
    role: str
    
    class Config:
        orm_mode = True


#-------------CURVE SCHEMAS--------------#
class Curve_value_out(BaseModel):
    curve_id: str
    md: float
    cal_value: float | None 
    well_id: str
    
    class Config:
        orm_mode = True
