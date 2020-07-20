from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.sql.sqltypes import REAL

Base = declarative_base()


# как описывать таблицы
class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False, unique=True)


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    member_name = Column(String, nullable=False)
    factor = Column(REAL, CheckConstraint(
        'factor <= 1.0 AND factor >= 0.0'), nullable=False)
    number_team = Column(Integer, nullable=False)


class Stats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, nullable=False)
    sprint_name = Column(String, nullable=False)
    result = Column(Integer, nullable=False)


class LoginPassword(Base):
    __tablename__ = 'login_password'
    id = Column(Integer, primary_key=True)
    userlogin = Column(String, nullable=False, unique=True)
    userpassword = Column(String, nullable=False)
    id_command = Column(Integer, nullable=False)

def create_db(engine):
    Base.metadata.create_all(engine)
