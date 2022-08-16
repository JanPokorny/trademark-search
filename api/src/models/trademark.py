import sqlalchemy
import sqlalchemy.orm
import pydantic
import datetime

from ..database import Base


class TrademarkORM(Base):
    __tablename__ = "trademarks"
    application_number = sqlalchemy.Column(sqlalchemy.String(9), primary_key=True)
    word_mark_text = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    application_date = sqlalchemy.Column(sqlalchemy.Date)
    registration_date = sqlalchemy.Column(sqlalchemy.Date)
    expiry_date = sqlalchemy.Column(sqlalchemy.Date)
    word_mark_text_matchable = sqlalchemy.Column(sqlalchemy.String(255), nullable=False, server_default="")


class TrademarkDTO(pydantic.BaseModel):
    application_number: str
    word_mark_text: str
    application_date: datetime.date | None = None
    registration_date: datetime.date | None = None
    expiry_date: datetime.date | None = None

    class Config:
        orm_mode = True
