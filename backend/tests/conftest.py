import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from db import models  # noqa: F401 — registers tables with metadata


@pytest.fixture
def db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def engine(db_path):
    eng = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    with Session(engine) as sess:
        yield sess


@pytest.fixture
def client(db_path, monkeypatch):
    monkeypatch.setattr("config.settings.db_path", db_path)
    # Reset engine so it uses the test db_path
    import db.database as db_mod
    db_mod._engine = None

    from main import app
    with TestClient(app) as c:
        yield c
    db_mod._engine = None
