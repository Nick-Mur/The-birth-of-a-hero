import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Inventory(SqlAlchemyBase):
    __tablename__ = 'inventory'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    slot_1 = sqlalchemy.Column(sqlalchemy.String, default='')
    slot_2 = sqlalchemy.Column(sqlalchemy.String, default='')
    slot_3 = sqlalchemy.Column(sqlalchemy.String, default='')
    slot_4 = sqlalchemy.Column(sqlalchemy.String, default='')


    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="inventory")

    def __repr__(self):
        return '<Inventory %r>' % self.id
