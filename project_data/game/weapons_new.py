from project_data.game.techniques import *

from random import choice


class Weapon:
    def __init__(self, name, damage, w_range, techniques, description):
        self.name = name
        self.damage = damage
        self.w_range = w_range
        self.techniques = techniques
        self.description = description

    def info(self, id=None, full=True):
        text = '+=={:::::::::::::::::> |WEAPON|\n' \
               '- - - - - - - - - - - - - - - - - - - - - -' \
               f'\n🪧 Название: {self.name}\n' \
               f'\n🩸 Урон: {self.damage}\n' \
               f'👊 Связанные приёмы:\n'
        for i in self.techniques:
            text += f'• {i.name}\n'
        text += f'\n📜 Описание: {self.description}\n' \
                f'- - - - - - - - - - - - - - - - - - - - - -'

        return text


hero_sword = Weapon(name='Меч героя', damage=4, w_range=0, techniques=[],
description='Этот меч был дан тебе для свершения великих дел. Он не так хорош, как выглядит, зато красиво блестит.')

dagger = Weapon(name='Скрытый клинок', damage=3, w_range=0, techniques=[knife_throwing],
description='Некоторые люди ради таких клинков отрубали себя безымянный палец!')
weapons_name_to_object = {'Меч героя': hero_sword,
                          'Скрытый клинок': dagger}
