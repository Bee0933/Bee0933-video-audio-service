from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String
import os


DB_USR = os.environ.get("DB_USR")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# connection_string = os.environ.get("DB_URL")
connection_string = f"postgresql+psycopg2://{DB_USR}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

engine = create_engine(url=connection_string, echo=True)

Sessionlocal = scoped_session(sessionmaker(bind=engine))

# model
class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(), unique=True)
    password = Column(String())


def create_db():
    Base.metadata.create_all(bind=engine)


# def populate_db(usr_email: str, usr_password: str):
#     new_user = user(email=usr_email, password=usr_password)
#     with Sessionlocal() as db:
#         db.add(new_user)
#         db.commit()
