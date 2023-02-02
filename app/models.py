from database import Base, metadata

class User(Base):
     __table__ = metadata.tables['user']
     
class Curve_value(Base):
     __table__ = metadata.tables['cal_curve_value']
     
     