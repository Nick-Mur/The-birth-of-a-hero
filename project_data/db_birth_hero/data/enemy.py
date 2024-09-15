import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Enemy(SqlAlchemyBase):
    __tablename__ = 'enemy'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, default='Разбойник (Алчек)')
    health = sqlalchemy.Column(sqlalchemy.Integer, default=40)
    defence = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    techniques_dice = sqlalchemy.Column(sqlalchemy.String, default='d4')

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="enemy")

    def __repr__(self):
        return '<Enemy %r>' % self.id
