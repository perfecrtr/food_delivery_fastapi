from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Null

class Base(DeclarativeBase):
    type_annotation_map = {
        None: Null
    }