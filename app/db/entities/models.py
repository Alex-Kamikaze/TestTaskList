from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer, Uuid, ForeignKey
from uuid import uuid4


class Base(DeclarativeBase): ...


class Status(Base):
    """Статусы задачи"""

    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=2048))
    tasks = relationship("Task", back_populates="status")

    def __repr__(self):
        return self.name


class Task(Base):
    __tablename__ = "task"

    id = Column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    name = Column(String(length=2048))
    text = Column(String(length=4096))
    status_id = Column(ForeignKey("status.id"))
    status = relationship("Status", back_populates="tasks")

    def __repr__(self):
        return self.name
