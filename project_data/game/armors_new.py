from project_data.game.specials import *


from random import choice
class Armor:
    def __init__(self, name, defence, special, description):
        self.name = name
        self.defence = defence
        self.special = special
        self.description = description

    def info(self, id=None, full=True):
        text = '+=={:::::::::::::::::> |ARMOR|\n' \
               '- - - - - - - - - - - - - - - - - - - - - -' \
               f'\n🪧 Название: {self.name}\n' \
               f'\n🛡️ Защита: {self.defence}\n' \
               f'🌟 Особенность: {self.special.name}\n' \
               f'\n📜 Описание: {self.description}\n' \
               f'- - - - - - - - - - - - - - - - - - - - - -'
        return text

shining_armour = Armor(name='Сияющие доспехи', defence=10, special=prudence, description=
'Прекрасные сияющие доспехи, они сами появились на тебе, благодаря воле небес. Правда, всё равно до конца не понятно,'
' куда делась старая одежда...')


mothwing_cloak = Armor(name='Накидка мотылька', defence=0, special=adventurism, description=
'Говорят, раньше в ней ходили рыцари с гвоздями.')


armors_name_to_object = {'Сияющие доспехи': shining_armour,
                         'Накидка мотылька': mothwing_cloak}
