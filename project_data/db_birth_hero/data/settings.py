import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Settings(SqlAlchemyBase):
    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    userID = sqlalchemy.Column(sqlalchemy.Integer,
                               index=True, unique=True, nullable=True)
    buy_the_game = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    time_sleep = sqlalchemy.Column(sqlalchemy.Integer, default=3)

    morality = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    reputation_tavern_keeper = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    reputation_storyteller = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    special_situation = sqlalchemy.Column(sqlalchemy.String, default='')
    stage = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    choices = sqlalchemy.Column(sqlalchemy.String, default='')

    save = sqlalchemy.Column(sqlalchemy.String, default='')

    key_plot = sqlalchemy.Column(sqlalchemy.String, default='start')
    key_markup = sqlalchemy.Column(sqlalchemy.String, default='start')

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    hero = orm.relationship("Hero", back_populates='settings')
    enemy = orm.relationship("Enemy", back_populates='settings')
    inventory = orm.relationship("Inventory", back_populates='settings')
    fight = orm.relationship("Fight", back_populates='settings')
    techniques = orm.relationship("Techniques", back_populates='settings')
    magic = orm.relationship("Magic", back_populates='settings')

    def __repr__(self):
        return '<Settings %r>' % self.id