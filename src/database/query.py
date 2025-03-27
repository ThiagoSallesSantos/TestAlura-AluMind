## Description: This file contains the query functions for the database

from functools import singledispatch

from sqlalchemy.orm import Session
from sqlalchemy import text, Result

from src.database.models import Base, Feedback

from datetime import datetime

from typing import List, Union

@singledispatch
def add_db(data: Base, *, session: Session) -> None:
    session.add(data)
    session.commit()

@add_db.register(list)
def add_db_list(list_of_data: List[Base], *, session: Session) -> None:
    for data in list_of_data:
        session.add(data)
    session.commit()

def get_db(table: Base, *, session: Session, get_all: bool = True, **kwargs) -> Union[List[Base], Base, None]:
    if get_all:
        return session.query(table).filter_by(**kwargs).all()
    return session.query(table).filter_by(**kwargs).first()

def delete_db(table: Base, *, session: Session, **kwargs) -> None:
    session.query(table).filter_by(**kwargs).delete()
    session.commit()

def query_db(query: str, session: Session) -> Result:
    return session.execute(text(query))

def get_after_that(session: Session, after_that: datetime) -> List[Feedback]:
    return session.query(Feedback).filter(Feedback.feedback_created_at >= after_that).all()
