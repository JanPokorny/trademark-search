import sqlalchemy
import sqlalchemy.ext.declarative

from .config import PostgresConfig

postgres_config = PostgresConfig.from_environ()

engine = sqlalchemy.create_engine(
    f"postgresql://{postgres_config.USER}:{postgres_config.PASSWORD}@{postgres_config.HOST}/{postgres_config.DB}"
)
SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = sqlalchemy.ext.declarative.declarative_base()
