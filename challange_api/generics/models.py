import sqlalchemy.exc
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from challange_api.utils.shortcuts import uuid_url64


engine = create_engine("sqlite:///database.db")
# engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    session = Session()
    try:
        yield session
    except StopIteration:
        ...
    finally:
        session.close()


class Manager:

    def __init__(self, model):
        self.__model = model
        self.__session = next(get_db_session())

    @property
    def model(self):
        return self.__model

    @property
    def session(self):
        return self.__session

    def all(self, limit: int = 10, offset: int = 0):
        return self.session.query(self.model).offset(offset).limit(limit).all()

    def get(self, pk: str | None = None, *args, **kwargs):
        if kwargs:
            return self.session.query(self.model).filter_by(**kwargs).first()
        return self.session.query(self.model).get(pk)

    def create(self, body: BaseModel):
        try:
            data = self.model(**body.model_dump())
            self.session.add(data)
            self.session.commit()
            self.session.refresh(data)
        except sqlalchemy.exc.IntegrityError as err:
            error = [e for e in err.args]
            self.session.rollback()
            raise HTTPException(status_code=400, detail=error)
        return data

    def update(self, instance, data: BaseModel):
        obj_data = jsonable_encoder(instance)
        data = data.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in data:
                setattr(instance, field, data[field])
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def delete(self, instance):
        self.session.delete(instance)
        self.session.commit()


class Model(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, unique=True, default=uuid_url64)

    @classmethod
    def objects(cls):
        return Manager(cls)

    class Meta:
        abstract = True



