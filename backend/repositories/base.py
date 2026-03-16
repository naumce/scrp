from typing import Generic, TypeVar, Optional

from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)


class Repository(Generic[T]):
    def __init__(self, model: type[T], session: Session):
        self._model = model
        self._session = session

    def find_all(self) -> list[T]:
        statement = select(self._model)
        return list(self._session.exec(statement).all())

    def find_by_id(self, id: int) -> Optional[T]:
        return self._session.get(self._model, id)

    def create(self, data: dict) -> T:
        instance = self._model(**data)
        self._session.add(instance)
        self._session.commit()
        self._session.refresh(instance)
        return instance

    def update(self, id: int, data: dict) -> Optional[T]:
        instance = self._session.get(self._model, id)
        if instance is None:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        self._session.add(instance)
        self._session.commit()
        self._session.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self._session.get(self._model, id)
        if instance is None:
            return False
        self._session.delete(instance)
        self._session.commit()
        return True
