# coding: utf-8
from db import Session
from datetime import datetime


def add_model(model):
    with Session() as session:
        session.add(model)
        session.commit()


def get_model_by_id(model, mid):
    with Session() as session:
        return session.query(model). \
            filter(model.id == mid). \
            first()


def update_model_by_id(model, mid, **kwargs):
    kwargs["updated_at"] = datetime.now()
    with Session() as session:
        session.query(model).where(model.id == mid).update(kwargs)
        session.commit()


def delete_model_by_id(model, mid):
    with Session() as session:
        session.query(model).where(model.id == mid).delete()
        session.commit()
