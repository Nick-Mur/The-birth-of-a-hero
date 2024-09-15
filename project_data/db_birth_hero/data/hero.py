import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Hero(SqlAlchemyBase):
    __tablename__ = 'hero'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, default='')

    max_health = sqlalchemy.Column(sqlalchemy.Integer, default=30)
    health = sqlalchemy.Column(sqlalchemy.Integer, default=30)
    max_defence = sqlalchemy.Column(sqlalchemy.Integer, default=10)
    defence = sqlalchemy.Column(sqlalchemy.Integer, default=10)

    cash = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    equipped_weapon = sqlalchemy.Column(sqlalchemy.String, default='Меч героя')
    equipped_armor = sqlalchemy.Column(sqlalchemy.String, default='Сияющие доспехи')

    battle_level = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    magic_level = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    techniques_dice = sqlalchemy.Column(sqlalchemy.String, default='d4')

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="hero")

    def __repr__(self):
        return '<Hero %r>' % self.id