from .models.trademark import TrademarkORM
import sqlalchemy


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
