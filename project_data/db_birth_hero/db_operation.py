from datetime import datetime

from sqlalchemy.exc import IntegrityError

from project_data.db_birth_hero.data.settings import Settings
from project_data.db_birth_hero.data.hero import Hero
from project_data.db_birth_hero.data.enemy import Enemy
from project_data.db_birth_hero.data.inventory import Inventory
from project_data.db_birth_hero.data.fight import Fight
from project_data.db_birth_hero.data.techniques import Techniques
from project_data.db_birth_hero.data.magic import Magic


def db_reg(userid):
    try:
        from project_data.db_birth_hero.data import db_session
        db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")

        settings = Settings()
        settings.userID = userid

        hero = Hero()
        settings.hero.append(hero)

        enemy = Enemy()
        settings.enemy.append(enemy)

        inventory = Inventory()
        settings.inventory.append(inventory)

        fight = Fight()
        settings.fight.append(fight)

        techniques = Techniques()
        settings.techniques.append(techniques)

        magic = Magic()
        settings.magic.append(magic)

        db_sess = db_session.create_session()
        db_sess.add(settings)
        db_sess.commit()
        db_sess.close()
    except IntegrityError:
        pass


# region save
def save_enemy(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.enemy:
        if param == 'name':
            settings.enemy[0].name = val
        elif param == 'health':
            settings.enemy[0].health = val
        elif param == 'defence':
            settings.enemy[0].defence = val
        elif param == 'techniques_dice':
            settings.enemy[0].techniques_dice = val
    db_sess.commit()
    db_sess.close()


def save_fight(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.fight:
        if 'sequence' in param:
            if 'self_sequence' in param:
                if settings.fight[0].self_sequence == '' or param[0] == '-' : settings.fight[0].self_sequence = val
                else: settings.fight[0].self_sequence += f', {val}'
            else:
                if settings.fight[0].enemy_sequence == '' or param[0] == '-': settings.fight[0].enemy_sequence = val
                else: settings.fight[0].enemy_sequence += f', {val}'
        if 'points' in param:
            if 'self_points' in param:
                if param[0] == '+': settings.fight[0].self_points += val
                elif param[0] == '-': settings.fight[0].self_points -= val
                else: settings.fight[0].self_points = val
            else:
                if param[0] == '+': settings.fight[0].enemy_points += val
                elif param[0] == '-': settings.fight[0].enemy_points -= val
                else: settings.fight[0].enemy_points = val
        elif param == 'self_armor_bonus':
            settings.fight[0].self_armor_bonus = val
        elif param == 'enemy_armor_bonus':
            settings.fight[0].enemy_armor_bonus = val
        elif param == 'roll_dice':
            settings.fight[0].roll_dice = val
        elif param == 'distance':
            settings.fight[0].distance = val
        elif param == '+distance':
            settings.fight[0].distance += val
        elif param == '-distance':
            settings.fight[0].distance -= val
        elif param == 'move':
            settings.fight[0].move = val
        elif param == '+move':
            settings.fight[0].move += val
    db_sess.commit()
    db_sess.close()


def save_hero(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.hero:
        if param == 'name':
            settings.hero[0].name = val
        elif param == 'max_health':
            settings.hero[0].max_health = val
        elif param == 'health':
            settings.hero[0].health = val
        elif param == 'max_defence':
            settings.hero[0].max_defence = val
        elif param == 'defence':
            settings.hero[0].defence = val
        elif param == 'cash':
            settings.hero[0].cash = val
        elif param == 'equipped_weapon':
            settings.hero[0].equipped_weapon = val
        elif param == 'equipped_armor':
            settings.hero[0].equipped_armor = val
        elif param == 'magic_level':
            settings.hero[0].magic_level = val
        elif param == 'battle_level':
            settings.hero[0].battle_level = val
        elif param == 'techniques_dice':
            settings.hero[0].techniques_dice = val
    db_sess.commit()
    db_sess.close()


def save_inventory(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.inventory:
        if param == 'slot_1':
            settings.inventory[0].slot_1 = val
        elif param == 'slot_2':
            settings.inventory[0].slot_2 = val
        elif param == 'slot_3':
            settings.inventory[0].slot_3 = val
        elif param == 'slot_4':
            settings.inventory[0].slot_4 = val
    db_sess.commit()
    db_sess.close()


def save_settings(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if 'reputation_storyteller' in param:
        if param[0] == '+': settings.reputation_storyteller += val
        elif param[0] == '-': settings.reputation_storyteller -= val
        else: settings.reputation_storyteller = val
    elif param == 'reputation_tavern_keeper':
        settings.reputation_tavern_keeper = val
    elif param == 'morality':
        settings.morality = val
    elif 'special_situation' in param:
        if param[0] == '-': settings.special_situation = settings.special_situation.removesuffix(val)
        elif settings.special_situation == '': settings.special_situation = val
        else: settings.special_situation += f', {val}'
    elif param == 'choices':
        if settings.choices == '':
            settings.choices = val
        else:
            settings.choices += f', {val}'
    elif param == 'buy_the_game':
        settings.buy_the_game = val
    elif param == 'time_sleep':
        settings.time_sleep = val
    elif param == 'key_plot':
        settings.key_plot = val
    elif param == 'key_markup':
        settings.key_markup = val
    elif param == 'time_sleep':
        settings.time_sleep = val
    db_sess.commit()
    db_sess.close()


def save_stage(userid, val):
    """Сохраняет значение stage"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    settings.stage = val
    db_sess.commit()
    db_sess.close()


def save_magic(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.magic:
        if param == 'slot_1':
            settings.magic[0].slot_1 = val
        elif param == 'slot_2':
            settings.magic[0].slot_2 = val
        elif param == 'slot_3':
            settings.magic[0].slot_3 = val
        elif param == 'slot_4':
            settings.magic[0].slot_4 = val
    db_sess.commit()
    db_sess.close()


def save_techniques(userid, param, val):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    if settings.techniques:
        if param == 'slot_1':
            settings.techniques[0].slot_1 = val
        elif param == 'slot_2':
            settings.techniques[0].slot_2 = val
        elif param == 'slot_3':
            settings.techniques[0].slot_3 = val
        elif param == 'slot_4':
            settings.techniques[0].slot_4 = val
    db_sess.commit()
    db_sess.close()


def save_all(userid):
    """Сохраняет значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()

    enemy = f"{settings.enemy[0].name},{settings.enemy[0].health},{settings.enemy[0].defence},{settings.enemy[0].techniques_dice}"

    hero = f"{settings.hero[0].name},{settings.hero[0].max_health},{settings.hero[0].health}," \
           f"{settings.hero[0].max_defence},{settings.hero[0].defence},{settings.hero[0].cash}," \
           f"{settings.hero[0].equipped_weapon},{settings.hero[0].equipped_armor},{settings.hero[0].battle_level}," \
           f"{settings.hero[0].magic_level},{settings.hero[0].techniques_dice}"

    inventory = f'{settings.inventory[0].slot_1},{settings.inventory[0].slot_2},' \
              f'{settings.inventory[0].slot_3},{settings.inventory[0].slot_4}'

    magic = f'{settings.magic[0].slot_1},{settings.magic[0].slot_2},' \
            f'{settings.magic[0].slot_3},{settings.magic[0].slot_4}'

    techniques = f'{settings.techniques[0].slot_1},{settings.techniques[0].slot_2},' \
            f'{settings.techniques[0].slot_3},{settings.techniques[0].slot_4}'

    fight = f"{settings.fight[0].self_sequence},{settings.fight[0].enemy_sequence},{settings.fight[0].self_points}," \
            f"{settings.fight[0].enemy_points},{settings.fight[0].self_armor_bonus},{settings.fight[0].enemy_armor_bonus}," \
            f"{settings.fight[0].roll_dice},{settings.fight[0].distance},{settings.fight[0].move}"
    user_settings = f"{settings.morality},{settings.reputation_tavern_keeper},{settings.special_situation}," \
               f"{settings.stage},{settings.choices},{settings.key_plot},{settings.key_markup},{settings.reputation_storyteller}"

    val = f"{enemy}|{hero}|{inventory}|{magic}|{techniques}|{fight}|{user_settings}"
    settings.save = val
    db_sess.commit()
    db_sess.close()


def load_all(userid):
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()

    # region load
    enemy, hero, inventory, magic, techniques, fight, user_settings = settings.save.split('|')
    enemy, hero, inventory, magic, techniques, fight, user_settings = enemy.split(','), hero.split(','), inventory.split(','), \
    magic.split(','), techniques.split(','), fight.split(','), user_settings.split(',')
    # endregion
    # region enemy
    settings.enemy[0].name = enemy[0]
    settings.enemy[0].health = int(enemy[1])
    settings.enemy[0].defence = int(enemy[2])
    settings.enemy[0].techniques_dice = enemy[3]
    # endregion
    # region hero
    settings.hero[0].name = hero[0]
    settings.hero[0].max_health = int(hero[1])
    settings.hero[0].health = int(hero[2])
    settings.hero[0].max_defence = int(hero[3])
    settings.hero[0].defence = int(hero[4])
    settings.hero[0].cash = int(hero[5])
    settings.hero[0].equipped_weapon = hero[6]
    settings.hero[0].equipped_armor = hero[7]
    settings.hero[0].battle_level = int(hero[8])
    settings.hero[0].magic_level = int(hero[9])
    settings.hero[0].techniques_dice = hero[10]
    # endregion

    settings.inventory[0].slot_1, settings.inventory[0].slot_2, settings.inventory[0].slot_3, \
        settings.inventory[0].slot_4 = inventory

    settings.magic[0].slot_1, settings.magic[0].slot_2, settings.magic[0].slot_3, settings.magic[0].slot_4 = magic

    settings.techniques[0].slot_1, settings.techniques[0].slot_2, settings.techniques[0].slot_3, \
        settings.techniques[0].slot_4 = techniques

    settings.fight[0].self_sequence = fight[0]
    settings.fight[0].enemy_sequence = fight[1]
    settings.fight[0].self_points = int(fight[2])
    settings.fight[0].enemy_points = int(fight[3])
    settings.fight[0].self_armor_bonus = fight[4]
    settings.fight[0].enemy_armor_bonus = fight[5]
    if fight[6] == 'True': settings.fight[0].roll_dice = True
    else: settings.fight[0].roll_dice = False
    settings.fight[0].distance = int(fight[7])
    settings.fight[0].move = int(fight[8])

    settings.morality = int(user_settings[0])
    settings.reputation_tavern_keeper = int(user_settings[1])
    settings.special_situation = user_settings[2]
    settings.stage = int(user_settings[3])
    settings.choices = user_settings[4]
    settings.key_plot = user_settings[5]
    settings.key_markup = user_settings[6]
    settings.reputation_storyteller = int(user_settings[7])

    db_sess.commit()
    db_sess.close()

def start_over(userid):
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()

    settings.enemy[0].name = 'Разбойник (Алчек)'
    settings.enemy[0].health = 40
    settings.enemy[0].defence = 0
    settings.enemy[0].techniques_dice = 'd4'

    settings.fight[0].self_sequence = ''
    settings.fight[0].enemy_sequence = ''
    settings.fight[0].self_points = 0
    settings.fight[0].enemy_points = 0
    settings.fight[0].self_armor_bonus = ''
    settings.fight[0].enemy_armor_bonus = ''
    settings.fight[0].roll_dice = False
    settings.fight[0].distance = 0
    settings.fight[0].move = 1

    settings.hero[0].name = ''
    settings.hero[0].max_health = 30
    settings.hero[0].health = 30
    settings.hero[0].max_defence = 10
    settings.hero[0].defence = 10
    settings.hero[0].cash = 0
    settings.hero[0].equipped_weapon = 'Меч героя'
    settings.hero[0].equipped_armor = 'Сияющие доспехи'
    settings.hero[0].battle_level = 0
    settings.hero[0].magic_level = 0
    settings.hero[0].techniques_dice = 'd4'

    settings.inventory[0].slot_1 = '—'
    settings.inventory[0].slot_2 = '—'
    settings.inventory[0].slot_3 = '—'
    settings.inventory[0].slot_4 = '—'

    settings.magic[0].slot_1 = '—'
    settings.magic[0].slot_2 = '—'
    settings.magic[0].slot_3 = '—'
    settings.magic[0].slot_4 = '—'

    settings.techniques[0].slot_1 = 'Удар героя'
    settings.techniques[0].slot_2 = 'Защитная стойка'
    settings.techniques[0].slot_3 = '—'
    settings.techniques[0].slot_4 = '—'

    settings.morality = 0
    settings.reputation_tavern_keeper = 0
    settings.reputation_storyteller = 0
    settings.special_situation = ''
    settings.stage = 1
    settings.choices = ''
    settings.key_plot = 'start'
    settings.key_markup = 'start'

    db_sess.commit()
    db_sess.close()

# endregion
# region get
def get_enemy(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.enemy:
        if param == 'name':
            result = settings.enemy[0].name
        elif param == 'health':
            result = settings.enemy[0].health
        elif param == 'defence':
            result = settings.enemy[0].defence
        elif param == 'techniques_dice':
            result = settings.enemy[0].techniques_dice
    db_sess.commit()
    db_sess.close()
    return result


def get_fight(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.fight:
        if 'sequence' in param:
            if param == 'self_sequence': result = settings.fight[0].self_sequence
            else: result = settings.fight[0].enemy_sequence
        elif 'points' in param:
            if 'self_points' in param:
                if param[0] == '+': result += settings.fight[0].self_points
                elif param[0] == '-': result -= settings.fight[0].self_points
                else: result = settings.fight[0].self_points
            else:
                if param[0] == '+': result += settings.fight[0].enemy_points
                elif param[0] == '-': result -= settings.fight[0].enemy_points
                else: result = settings.fight[0].enemy_points
        elif param == 'self_armor_bonus':
            result = settings.fight[0].self_armor_bonus
        elif param == 'enemy_armor_bonus':
            result = settings.fight[0].enemy_armor_bonus
        elif param == 'roll_dice':
            result = settings.fight[0].roll_dice
        elif param == 'dice':
            result = settings.fight[0].dice
        elif param == 'distance': result = settings.fight[0].distance
        elif param == 'move': result = settings.fight[0].move

    db_sess.commit()
    db_sess.close()
    return result


def get_hero(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.hero:
        if param == 'max_health':
            result = settings.hero[0].max_health
        elif param == 'health':
            result = settings.hero[0].health
        elif param == 'max_defence':
            result = settings.hero[0].max_defence
        elif param == 'defence':
            result = settings.hero[0].defence
        elif param == 'cash':
            result = settings.hero[0].cash
        elif param == 'name':
            result = settings.hero[0].name
        elif param == 'equipped_weapon':
            result = settings.hero[0].equipped_weapon
        elif param == 'equipped_armor':
            result = settings.hero[0].equipped_armor
        elif param == 'magic_level':
            result = settings.hero[0].magic_level
        elif param == 'battle_level':
            result = settings.hero[0].battle_level
        elif param == 'techniques_dice':
            result = settings.hero[0].techniques_dice
    db_sess.commit()
    db_sess.close()
    return result


def get_inventory(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.inventory:
        if param == 'slot_1':
            result = settings.inventory[0].slot_1
        elif param == 'slot_2':
            result = settings.inventory[0].slot_2
        elif param == 'slot_3':
            result = settings.inventory[0].slot_3
        elif param == 'slot_4':
            result = settings.inventory[0].slot_4
        elif param == 'all':
            result = [settings.inventory[0].slot_1, settings.inventory[0].slot_2,
                      settings.inventory[0].slot_3, settings.inventory[0].slot_3]
    db_sess.commit()
    db_sess.close()
    return result


def get_settings(userid, param):
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if param == 'reputation':
        result = settings.reputation
    elif param == 'special_situation':
        result = settings.special_situation
    elif param == 'choices':
        result = settings.choices
    elif param == 'time_sleep':
        result = settings.time_sleep
    elif param == 'key_plot':
        result = settings.key_plot
    elif param == 'key_markup':
        result = settings.key_markup
    elif param == 'save': result = settings.save
    db_sess.commit()
    db_sess.close()
    return result


def get_stage(userid):
    """Выводит значение stage"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    stage = settings.stage
    db_sess.close()
    return stage


def get_techniques(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.techniques:
        if param == 'slot_1':
            result = settings.techniques[0].slot_1
        elif param == 'slot_2':
            result = settings.techniques[0].slot_2
        elif param == 'slot_3':
            result = settings.techniques[0].slot_3
        elif param == 'slot_4':
            result = settings.techniques[0].slot_4
        elif param == 'all':
            result = [settings.techniques[0].slot_1, settings.techniques[0].slot_2,
                      settings.techniques[0].slot_3, settings.techniques[0].slot_4]
    db_sess.commit()
    db_sess.close()
    return result


def get_magic(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.magic:
        if param == 'slot_1':
            result = settings.magic[0].slot_1
        elif param == 'slot_2':
            result = settings.magic[0].slot_2
        elif param == 'slot_3':
            result = settings.magic[0].slot_3
        elif param == 'slot_4':
            result = settings.magic[0].slot_4
        elif param == 'all':
            result = [settings.magic[0].slot_1, settings.magic[0].slot_2,
                      settings.magic[0].slot_3, settings.magic[0].slot_4]
    db_sess.commit()
    db_sess.close()
    return result


def get_players_saves(userid, param):
    """Выводит значение блоков"""
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()
    result = ''
    if settings.players_saves:
        if param == 'slot_1':
            result = settings.players_saves[0].slot_1
        elif param == 'slot_2':
            result = settings.players_saves[0].slot_2
        elif param == 'slot_3':
            result = settings.players_saves[0].slot_3
        elif param == 'short_show':
            all_params = settings.players_saves[0].slot_1
            if all_params != '—':
                time = all_params.split('|')[0]
                hero = all_params.split('|')[3].split(',')
                name = hero[0]
                max_health = hero[1]
                health = hero[2]
                battle_level = hero[-2]
                if int(hero[-1]) == 0:
                    magic_level = ''
                else:
                    magic_level = f"✨ Магический уровень: {hero[-1]}"

                first = f"🪨 Первая печать\n" \
                        f"\n🕓 {time}\n" \
                        f"🪧 Имя: {name}\n" \
                        f"❤️ Здоровье: {health} из {max_health}\n" \
                        f"⭐ боевой уровень: {battle_level}\n" \
                        f"{magic_level}"
            else:
                first = '🪨 Первая печать\n' \
                        '—'

            all_params = settings.players_saves[0].slot_2
            if all_params != '—':
                time = all_params.split('|')[0]
                hero = all_params.split('|')[3].split(',')
                name = hero[0]
                max_health = hero[1]
                health = hero[2]
                battle_level = hero[-2]
                if int(hero[-1]) == 0:
                    magic_level = ''
                else:
                    magic_level = f"✨ Магический уровень: {hero[-1]}"

                second = f"🪨 Вторая печать\n" \
                         f"\n🕓 {time}\n" \
                         f"🪧 Имя: {name}\n" \
                         f"❤️ Здоровье: {health} из {max_health}\n" \
                         f"⭐ боевой уровень: {battle_level}\n" \
                         f"{magic_level}"
            else:
                second = '🪨 Вторая печать\n' \
                        '—'

            all_params = settings.players_saves[0].slot_3
            if all_params != '—':
                time = all_params.split('|')[0]
                hero = all_params.split('|')[3].split(',')
                name = hero[0]
                max_health = hero[1]
                health = hero[2]
                battle_level = hero[-2]
                if int(hero[-1]) == 0:
                    magic_level = ''
                else:
                    magic_level = f"✨ Магический уровень: {hero[-1]}"

                third = f"🪨 Третья печать\n" \
                        f"\n 🕓{time}\n" \
                        f"🪧 Имя: {name}\n" \
                        f"❤️ Здоровье: {health} из {max_health}\n" \
                        f"⭐ боевой уровень: {battle_level}\n" \
                        f"{magic_level}"
            else:
                third = '🪨 Третья печать\n' \
                        '—'
            result = [first, second, third]
    db_sess.commit()
    db_sess.close()
    return result


def use_seal(userid, param):
    from project_data.db_birth_hero.data import db_session
    db_session.global_init("project_data/db_birth_hero/db/data_birth_hero.db")
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter_by(userID=userid).first()

    save = get_players_saves(userid, param).split('|')
    if save == ['—']:
        return None

    enemy =  save[2].split(',')
    settings.enemy[0].name = enemy[0]
    settings.enemy[0].health = int(enemy[1])
    settings.enemy[0].defence = int(enemy[2])

    hero = save[3].split(',')
    settings.hero[0].name = hero[0]
    settings.hero[0].max_health = int(hero[1])
    settings.hero[0].health = int(hero[2])
    settings.hero[0].max_defence = int(hero[3])
    settings.hero[0].defence = int(hero[4])
    settings.hero[0].cash = int(hero[5])
    settings.hero[0].equipped_weapon = hero[6]
    settings.hero[0].equipped_armor = hero[7]
    settings.hero[0].battle_level = int(hero[8])
    settings.hero[0].magic_level = int(hero[9])

    inv_arm = save[4].split(',')
    settings.inventory_armors[0].slot_1 = inv_arm[0]
    settings.inventory_armors[0].slot_2 = inv_arm[1]
    settings.inventory_armors[0].slot_3 = inv_arm[2]

    inv_cns = save[5].split(',')
    settings.inventory_consumables[0].slot_1 = inv_cns[0]
    settings.inventory_consumables[0].slot_2 = inv_cns[1]
    settings.inventory_consumables[0].slot_3 = inv_cns[2]

    inv_wpn = save[6].split(',')
    settings.inventory_weapons[0].slot_1 = inv_wpn[0]
    settings.inventory_weapons[0].slot_2 = inv_wpn[1]
    settings.inventory_weapons[0].slot_3 = inv_wpn[2]

    magic = save[7].split(',')
    settings.magic[0].slot_1 = magic[0]
    settings.magic[0].slot_2 = magic[1]
    settings.magic[0].slot_3 = magic[2]
    settings.magic[0].slot_4 = magic[3]

    techniques = save[8].split(',')
    settings.techniques[0].slot_1 = techniques[0]
    settings.techniques[0].slot_2 = techniques[1]
    settings.techniques[0].slot_3 = techniques[2]
    settings.techniques[0].slot_4 = techniques[3]

    user_save = save[9].split(',')
    settings.reputation = int(user_save[0])
    settings.special_situation = user_save[1]
    settings.stage = int(user_save[2])
    settings.choices = user_save[3]

    db_sess.commit()
    db_sess.close()

    return get_players_saves(userid, param).split('|')[1]
