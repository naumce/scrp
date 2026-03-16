from repositories.project_repo import ProjectRepository


def test_create_project(session):
    repo = ProjectRepository(session)
    project = repo.create({
        "name": "Chicago Manufacturers",
        "keyword": "manufacturing",
        "location": "Chicago",
        "radius": 50.0,
    })
    assert project.id is not None
    assert project.name == "Chicago Manufacturers"
    assert project.keyword == "manufacturing"


def test_find_all_projects(session):
    repo = ProjectRepository(session)
    repo.create({"name": "P1", "keyword": "k1", "location": "L1"})
    repo.create({"name": "P2", "keyword": "k2", "location": "L2"})
    projects = repo.find_all()
    assert len(projects) == 2


def test_find_by_id(session):
    repo = ProjectRepository(session)
    created = repo.create({"name": "Test", "keyword": "k", "location": "L"})
    found = repo.find_by_id(created.id)
    assert found is not None
    assert found.name == "Test"


def test_find_by_id_not_found(session):
    repo = ProjectRepository(session)
    assert repo.find_by_id(999) is None


def test_update_project(session):
    repo = ProjectRepository(session)
    created = repo.create({"name": "Old", "keyword": "k", "location": "L"})
    updated = repo.update(created.id, {"name": "New"})
    assert updated is not None
    assert updated.name == "New"
    assert updated.keyword == "k"


def test_update_not_found(session):
    repo = ProjectRepository(session)
    assert repo.update(999, {"name": "X"}) is None


def test_delete_project(session):
    repo = ProjectRepository(session)
    created = repo.create({"name": "Del", "keyword": "k", "location": "L"})
    assert repo.delete(created.id) is True
    assert repo.find_by_id(created.id) is None


def test_delete_not_found(session):
    repo = ProjectRepository(session)
    assert repo.delete(999) is False
