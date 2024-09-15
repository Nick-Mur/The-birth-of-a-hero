from project_data.game.weapons_new import *
from project_data.game.armors_new import *
from project_data.game.techniques import *
from project_data.db_birth_hero.db_operation import *
from project_data.settings.fonts import *

from random import choice, randint


class Hero:
    def __init__(self, description):
        self.description = description
        self.class_name = 'Hero'

class Character:
    def __init__(self, name, health, techniques, weapon, armor, description):
        self.name = name
        self.health = health
        self.techniques = techniques
        self.weapon = weapon
        self.armor = armor
        self.defence = armor.defence
        self.description = description
        self.class_name = 'Enemy'


class Rogue(Character):
    def attack(self, id):
        points, distance = get_fight(id, 'enemy_points'), get_fight(id, 'distance')
        pattern = randint(1, 3)
        extra, steps_up = list(), list()
        if distance != 0:
            if distance == points:
                for _ in range(distance - 1): steps_up.append(step_up.use(self, id))
            else:
                for _ in range(distance): steps_up.append(step_up.use(self, id))

        if points:
            if points > 1 and pattern == 1:
                extra.append(knife_throwing.use(self, self.weapon, id))
                extra.append(thousand_and_one_strikes.use(self, self.weapon, id))
            elif pattern == 2:
                for _ in range(points): extra.append(thousand_and_one_strikes.use(self, self.weapon, id))
            elif points > 2 and pattern == 3:
                extra.append(thousand_and_one_strikes.use(self, self.weapon, id))
                extra.append(knife_throwing.use(self, self.weapon, id))
                extra.append(thousand_and_one_strikes.use(self, self.weapon, id))
            elif points < 3: extra.append('pass')
        save_fight(id, 'enemy_armor_bonus', str(get_fight(id, 'enemy_points')))
        return [steps_up, extra]


hero = Hero(description='Жил да был, как приключения вдруг настигли его')


rogue_name = underlined('Разбойник (Алчек)')
rogue = Rogue(name='Разбойник (Алчек)', health=40,
              techniques=[knife_throwing, thousand_and_one_strikes, '', ''],
              weapon=dagger, armor=mothwing_cloak,
              description='Некогда приличный человек, владелец таверны, не выдержавший ужаса войны')


enemies_name_to_object = {'Разбойник (Алчек)': rogue}
