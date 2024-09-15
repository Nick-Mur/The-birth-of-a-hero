from project_data.db_birth_hero.db_operation import *
from project_data.settings.fonts import *

from random import randint


class Special:
    def __init__(self, name, mechanics):
        self.name = name
        self.mechanics = mechanics



prudence = Special(
name='Благоразумие',
mechanics='Твои очки действия не сгорают в конце хода.')

adventurism = Special(
name='Авантюризм',
mechanics='Если оставить какое-то число о.п в конце хода, то на следующем ходу тебе выпадет не меньше этого числа или максимум на кубике.')

specials_name_to_object = {'Благоразумие': prudence,
                           'Авантюризм': adventurism}
