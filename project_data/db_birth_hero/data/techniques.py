import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Techniques(SqlAlchemyBase):
    __tablename__ = 'techniques'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    slot_1 = sqlalchemy.Column(sqlalchemy.String, default='Удар героя')
    slot_2 = sqlalchemy.Column(sqlalchemy.String, default='Защитная стойка')
    slot_3 = sqlalchemy.Column(sqlalchemy.String, default='—')
    slot_4 = sqlalchemy.Column(sqlalchemy.String, default='—')

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="techniques")

    def __repr__(self):
        return '<Techniques %r>' % self.id
