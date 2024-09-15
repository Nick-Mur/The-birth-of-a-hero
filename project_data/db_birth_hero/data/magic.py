import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Magic(SqlAlchemyBase):
    __tablename__ = 'magic'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    slot_1 = sqlalchemy.Column(sqlalchemy.String, default='—')
    slot_2 = sqlalchemy.Column(sqlalchemy.String, default='—')
    slot_3 = sqlalchemy.Column(sqlalchemy.String, default='—')
    slot_4 = sqlalchemy.Column(sqlalchemy.String, default='—')

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="magic")

    def __repr__(self):
        return '<Magic %r>' % self.id
