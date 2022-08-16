import fastapi
import sqlalchemy

from .models.trademark import TrademarkDTO

from .crud import get_trademarks_by_text, get_trademarks_by_fuzzy_text
from .database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)
app = fastapi.FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/trademarks", response_model=list[TrademarkDTO])
def get_trademark(text: str, fuzzy: bool = False, limit: int = 10, db: sqlalchemy.orm.Session = fastapi.Depends(get_db)):
    if fuzzy:
        return get_trademarks_by_fuzzy_text(db, text, limit)
    return get_trademarks_by_text(db, text)
