from sqlmodel import SQLModel, create_engine, Session

from config import settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        connect_args = {}
        if settings.is_sqlite:
            connect_args["check_same_thread"] = False

        _engine = create_engine(
            settings.effective_database_url,
            echo=False,
            connect_args=connect_args,
        )
    return _engine


async def init_db():
    engine = get_engine()
    if settings.is_sqlite:
        with engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL")
            conn.commit()
    SQLModel.metadata.create_all(engine)
    if settings.is_sqlite:
        _run_sqlite_migrations(engine)


def _run_sqlite_migrations(engine):
    """Add columns that may be missing from older SQLite databases."""
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
