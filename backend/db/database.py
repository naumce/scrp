from sqlmodel import SQLModel, create_engine, Session

from config import settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            f"sqlite:///{settings.db_path}",
            echo=False,
            connect_args={"check_same_thread": False},
        )
    return _engine


async def init_db():
    engine = get_engine()
    # Enable WAL mode for concurrent read/write safety
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL")
        conn.commit()
    SQLModel.metadata.create_all(engine)
    _run_migrations(engine)


def _run_migrations(engine):
    """Add columns that may be missing from older databases."""
    migrations = [
        ("businesses", "notes", "TEXT DEFAULT ''"),
        ("businesses", "lat", "REAL DEFAULT 0.0"),
        ("businesses", "lon", "REAL DEFAULT 0.0"),
    ]
    with engine.connect() as conn:
        for table, column, col_type in migrations:
            result = conn.exec_driver_sql(f"PRAGMA table_info({table})")
            existing = [row[1] for row in result]
            if column not in existing:
                conn.exec_driver_sql(
                    f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"
                )
        conn.commit()


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
