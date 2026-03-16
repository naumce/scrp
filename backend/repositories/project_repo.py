from sqlmodel import Session

from db.models import Project
from repositories.base import Repository


class ProjectRepository(Repository[Project]):
    def __init__(self, session: Session):
        super().__init__(Project, session)
