from project_data.db_birth_hero.db_operation import *
from project_data.settings.fonts import bold


class Techniques:
    def __init__(self, name, cost, mechanics):
        self.name = name
        self.cost = cost
        self.mechanics = mechanics
    

class HeroPunch(Techniques):
    def use(self, subject, weapon=None, id=None):
        weapon_range, distance = weapon.w_range, get_fight(id, 'distance')
        if weapon_range < distance: return 'Не хватает дальности оружия.'
        if get_fight(id, 'self_sequence') == '': cost = 0
        else: cost = self.cost
        if get_fight(id, 'self_points') < cost: return 'Не достаточно о.п.'
        damage, health, defence = weapon.damage, get_enemy(id, 'health'), get_enemy(id, 'defence')
        if defence > 0: defence -= damage
        else: health -= damage
        if len(get_fight(id, 'self_sequence').split(', ')) == 4: distance += 1
        save_fight(id, 'self_sequence', f'П:{self.name}')
        save_fight(id, '-self_points', cost)
        return [health, defence, distance, 'other', self.name]


class DefencePosture(Techniques):
    def use(self, subject, weapon=None, id=None):
        if get_fight(id, 'self_points') < self.cost: return 'Не достаточно о.п.'
        damage, health, defence = weapon.damage, get_hero(id, 'health'), get_hero(id, 'defence')
        save_fight(id, 'self_sequence', f'П:{self.name}')
        if len(get_fight(id, 'self_sequence').split(', ')) % 2 != 0: damage = damage * 3 // 2
        else: damage //= 2
        save_fight(id, '-self_points', 2)
        return [health, defence + damage, get_fight(id, 'distance'), 'self', self.name]


class KnifeThrowing(Techniques):
    def use(self, subject, weapon=None, id=None):
        if subject.class_name == 'Hero':
            pass
        else:
            damage, health, defence, points = weapon.damage, get_hero(id, 'health'), get_hero(id, 'defence'), get_fight(id, 'enemy_points')
            new_health, new_defence = health, defence
            if points > 1: damage = 2 * (points - 1)
            if defence > 0: new_defence = defence - damage
            else: new_health = health - damage
            for _ in range(points - 1): save_fight(id, 'enemy_sequence', f'П:{self.name}')
            save_fight(id, 'enemy_points', 1)
            save_hero(id, 'health', new_health)
            save_hero(id, 'defence', new_defence)
            return [health - new_health, defence - new_defence, 0, 'other', self.name]



class ThousandAndOneStrikes(Techniques):
    def use(self, subject, weapon=None, id=None):
        if subject.class_name == 'Hero':
            pass
        else:
            damage, health, defence, sequence = weapon.damage, get_hero(id, 'health'), get_hero(id, 'defence'), get_fight(id, 'enemy_sequence')
            new_health, new_defence = health, defence
            if sequence == '': damage *= 1.5
            else: damage = len(sequence.split(', ')) * 2
            if defence > 0: new_defence = defence - damage
            else: new_health = health - damage
            save_fight(id, 'enemy_sequence', f'П:{self.name}')
            save_fight(id, '-enemy_points', 1)
            save_hero(id, 'health', int(new_health))
            save_hero(id, 'defence', int(new_defence))
            return [int(health) - int(new_health), int(defence) - int(new_defence), 0, 'other', self.name]

class StepUp:
    def use(self, subject, id):
        save_fight(id, '-distance', 1)
        if subject.class_name == 'Hero':
            save_fight(id, '-self_points', 1)
            save_fight(id, 'self_sequence', f'Д:Подойти')
            return f'Герой решился подойти к противнику, сократив дистанцию на 1.\nТекущая дистанция: {get_fight(id, "distance")}.'
        else:
            save_fight(id, '-enemy_points', 1)
            save_fight(id, 'enemy_sequence', f'Д:Подойти')
            return f'{subject.name} подходит к герою, сократив дистанцию на 1.\nТекущая дистанция: {get_fight(id, "distance")}'


step_up = StepUp()


hero_punch = HeroPunch(name='Удар героя', cost=1, mechanics=
'Наносит обычный урон; дальность равна дальности оружия.\n'
'Если это первое действие за ход - стоимость равно 0, а если пятое - приём оттолкнёт противника на 1.')

defence_posture = DefencePosture(name='Защитная стойка', cost=2, mechanics=
'Если ход нечётный - приём даст защиту, равную 1.5x обычного урона. Иначе - половину.\n'
'Работает на любой дистанции.')

knife_throwing = KnifeThrowing(name='Метание ножей', cost='X - 1', mechanics=
'После использования оставляет 1 о.п.; дальность равна дальности оружия.\n'
'Наносит 2 ед. урона за каждое потраченное о.п. Каждое нанесение урона является действием.')

thousand_and_one_strikes = ThousandAndOneStrikes(name='Тысяча и один удар', cost=1, mechanics=
'Наносит 2 урона за каждый использованный приём за ход. Если это первое действие за ход - наносит 1.5x обычного урона.\n'
'Дальность равна дальности оружия.')
techniques_name_to_object = {'Удар героя': hero_punch,
                             'Защитная стойка': defence_posture,
                             'Метание ножей': knife_throwing,
                             'Тысяча и один удар': thousand_and_one_strikes}