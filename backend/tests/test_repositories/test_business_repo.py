from db.models import Project
from repositories.business_repo import BusinessRepository


def _create_project(session) -> Project:
    p = Project(name="Test", keyword="k", location="L")
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


def test_create_business(session):
    project = _create_project(session)
    repo = BusinessRepository(session)
    biz = repo.create({
        "project_id": project.id,
        "name": "ACME Corp",
        "address": "123 Main St",
        "website": "https://acme.com",
    })
    assert biz.id is not None
    assert biz.name == "ACME Corp"


def test_find_by_project(session):
    project = _create_project(session)
    repo = BusinessRepository(session)
    repo.create({"project_id": project.id, "name": "Biz1"})
    repo.create({"project_id": project.id, "name": "Biz2"})
    results = repo.find_by_project(project.id)
    assert len(results) == 2


def test_find_by_project_empty(session):
    repo = BusinessRepository(session)
    assert repo.find_by_project(999) == []


def test_create_many(session):
    project = _create_project(session)
    repo = BusinessRepository(session)
    items = [
        {"project_id": project.id, "name": f"Biz{i}"}
        for i in range(5)
    ]
    created = repo.create_many(items)
    assert len(created) == 5
    assert all(b.id is not None for b in created)


def test_toggle_favorite(session):
    project = _create_project(session)
    repo = BusinessRepository(session)
    biz = repo.create({"project_id": project.id, "name": "Fav"})
    assert biz.is_favorite is False

    toggled = repo.toggle_favorite(biz.id)
    assert toggled is not None
    assert toggled.is_favorite is True

    toggled2 = repo.toggle_favorite(biz.id)
    assert toggled2 is not None
    assert toggled2.is_favorite is False


def test_toggle_favorite_not_found(session):
    repo = BusinessRepository(session)
    assert repo.toggle_favorite(999) is None


def test_delete_business(session):
    project = _create_project(session)
    repo = BusinessRepository(session)
    biz = repo.create({"project_id": project.id, "name": "Del"})
    assert repo.delete(biz.id) is True
    assert repo.find_by_id(biz.id) is None
