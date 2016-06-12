# coding=utf-8
from sqlalchemy import create_engine, Column, Integer, String, Sequence, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from consts import DB_URI

eng = create_engine(DB_URI)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'),
                primary_key=True, autoincrement=True)
    name = Column(String(50))

Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)

Session = sessionmaker(bind=eng)
session = Session()

session.add_all([User(name=username)
                 for username in ('xiaoming', 'wanglang', 'lilei')])

session.commit()


def get_result(rs):
    print '-' * 20
    for user in rs:
        print user.name

rs = session.query(User).filter(
    text('id > 2 and id < 4')).order_by(text('id')).all()
get_result(rs)
rs = session.query(User).filter(text('id<:value and name=:name')).params(
    value=3, name='xiaoming').all()
get_result(rs)
rs = session.query(User).from_statement(
    text('SELECT * FROM users where name=:name')).params(name='wanglang').all()
get_result(rs)
