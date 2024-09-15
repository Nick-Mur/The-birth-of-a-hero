from project_data.db_birth_hero.db_operation import *
from project_data.game.enemies import  enemies_name_to_object
from random import choice


user_d4 = [1, 2, 2, 2, 3, 3, 3, 4, 4]
enemy_d4 = [1, 1, 2, 2, 2, 3, 3, 3, 4]
user_dices = {'d4': user_d4}
enemy_dices = {'d4': enemy_d4}


def self_points_after_move(id):
    if get_hero(id, 'equipped_armor') == 'Сияющие доспехи' and get_fight(id, 'self_points') > 0: save_fight(id, 'self_armor_bonus', 'True')
    else: save_fight(id, 'self_points', 0)

def enemy_points_after_move(id):
    save_fight(id, 'enemy_points', 0)


def self_points_before_move(id):
    dice, extra = user_dices[get_hero(id, 'techniques_dice')], ['self']
    points, bonus = choice(dice), get_fight(id, 'self_armor_bonus')
    if get_hero(id, 'equipped_armor') == 'Сияющие доспехи' and bonus == 'True':
        extra.append('Благоразумие')
        points = choice(dice)
    extra.append(points)
    return extra

def enemy_points_before_move(id):
    enemy, dice = enemies_name_to_object[get_enemy(id, 'name')], enemy_dices[get_enemy(id, 'techniques_dice')]
    points, bonus = choice(dice), get_fight(id, 'enemy_armor_bonus')
    extra = ['other']
    if enemy.armor.name == 'Накидка мотылька' and bonus.isdigit() and int(bonus) != 0:
        while points <= int(bonus) or points != max(dice): points = choice(dice)
        extra.append('Авантюризм')
    else:
        extra.append('')
        points = choice(dice)
    extra.append(points)
    return extra
