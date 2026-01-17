import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from app.logger import setup_logger

logger = setup_logger(__name__)

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        logger.warning("Factory for this db is already exist, skipping...")
        return

    if not db_file or not db_file.strip():
        logger.error("Database file not found.")
        raise FileNotFoundError("Database file not found.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    logger.info(f"Connecting to {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
