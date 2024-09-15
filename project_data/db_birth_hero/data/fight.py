import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Fight(SqlAlchemyBase):
    __tablename__ = 'fight'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    self_sequence = sqlalchemy.Column(sqlalchemy.String, default='')
    enemy_sequence = sqlalchemy.Column(sqlalchemy.String, default='')

    self_points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    enemy_points = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    self_armor_bonus = sqlalchemy.Column(sqlalchemy.String, default='')
    enemy_armor_bonus = sqlalchemy.Column(sqlalchemy.String, default='')

    roll_dice = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    distance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    move = sqlalchemy.Column(sqlalchemy.Integer, default=1)


    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("settings.userID"))
    settings = orm.relationship('Settings', back_populates="fight")

    def __repr__(self):
        return '<Fight %r>' % self.id
