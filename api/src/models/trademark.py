import datetime

import pydantic
import sqlalchemy
import sqlalchemy.orm

from ..database import Base

# More subdivision for such a small app didn't feel right, so I put all trademark-ops in this file


class TrademarkORM(Base):
    __tablename__ = "trademarks"
    application_number = sqlalchemy.Column(sqlalchemy.String(9), primary_key=True)
    word_mark_text = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    application_date = sqlalchemy.Column(sqlalchemy.Date)
    registration_date = sqlalchemy.Column(sqlalchemy.Date)
    expiry_date = sqlalchemy.Column(sqlalchemy.Date)
    word_mark_text_matchable = sqlalchemy.Column(
        sqlalchemy.String(255), nullable=False, server_default=""
    )


class TrademarkDTO(pydantic.BaseModel):
    application_number: str
    word_mark_text: str
    application_date: datetime.date | None = None
    registration_date: datetime.date | None = None
    expiry_date: datetime.date | None = None

    class Config:
        orm_mode = True


def get_trademarks_by_text(db: sqlalchemy.orm.Session, text: str):
    return db.query(TrademarkORM).where(TrademarkORM.word_mark_text == text).all()


def get_trademarks_by_fuzzy_text(
    db: sqlalchemy.orm.Session, text: str, limit: int = 10
) -> list[TrademarkORM]:
    return (
        db.query(TrademarkORM)
        .order_by(
            sqlalchemy.func.similarity(
                TrademarkORM.word_mark_text_matchable, sqlalchemy.func.matchable(text)
            ).desc()
        )
        .limit(limit)
        .all()
    )
