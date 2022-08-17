import fastapi
import sqlalchemy

from .database import Base, SessionLocal, engine
from .models.trademark import (
    TrademarkDTO,
    get_trademarks_by_fuzzy_text,
    get_trademarks_by_text,
)

Base.metadata.create_all(bind=engine)
app = fastapi.FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/trademarks", response_model=list[TrademarkDTO])
def get_trademark(
    text: str,
    fuzzy: bool = False,
    limit: int = 10,
    db: sqlalchemy.orm.Session = fastapi.Depends(get_db),
):
    """
    Retrieve trademarks by the text of the word mark, either exact or fuzzy match. Returns a list of trademarks, in descending order of similarity to the input text.

    Parameters:
    - `text` (str) - the text of the word mark (required)
    - `fuzzy` (bool, default False) - if True, perform fuzzy matching, otherwise perform exact matching (including case)
    - `limit` (int, default 10) - the maximum number of trademarks to return
    """
    if fuzzy:
        return get_trademarks_by_fuzzy_text(db, text, limit)
    return get_trademarks_by_text(db, text)
