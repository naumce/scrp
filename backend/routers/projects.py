from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from repositories.project_repo import ProjectRepository
from schemas.base import ok, err
from schemas.project import ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _repo(session: Session = Depends(get_session)) -> ProjectRepository:
    return ProjectRepository(session)


@router.get("/")
def list_projects(repo: ProjectRepository = Depends(_repo)):
    projects = repo.find_all()
    return ok([p.model_dump() for p in projects])


@router.get("/{project_id}")
def get_project(project_id: int, repo: ProjectRepository = Depends(_repo)):
    project = repo.find_by_id(project_id)
    if project is None:
        return err("Project not found")
    return ok(project.model_dump())


@router.post("/")
def create_project(
    data: ProjectCreate, repo: ProjectRepository = Depends(_repo)
):
    project = repo.create(data.model_dump())
    return ok(project.model_dump())


@router.put("/{project_id}")
def update_project(
    project_id: int,
    data: ProjectUpdate,
    repo: ProjectRepository = Depends(_repo),
):
    update_data = data.model_dump(exclude_unset=True)
    project = repo.update(project_id, update_data)
    if project is None:
        return err("Project not found")
    return ok(project.model_dump())


@router.delete("/{project_id}")
def delete_project(
    project_id: int, repo: ProjectRepository = Depends(_repo)
):
    deleted = repo.delete(project_id)
    if not deleted:
        return err("Project not found")
    return ok({"deleted": True})
