import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///FirstSteps\\blog.db")

#
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

#Configuraciones para sqlite
engine = create_engine(DATABASE_URL, echo=True, future=True, **engine_kwargs)

#crear una sesion por cada request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

# Modelo de BD de SQLAlchemist
class Base(DeclarativeBase):
    pass


#Iniciar sesion en DB
def get_db():
    db = SessionLocal()
    try:
        #yield, como return pero sin terminar la funcion
        yield db
    finally:
        db.close()