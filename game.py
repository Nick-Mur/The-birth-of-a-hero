import telebot
from telebot import types


from project_data.settings.config import bot_token
from project_data.db_birth_hero.db_operation import *
from project_data.game.enemies import enemies_name_to_object, hero
from project_data.game.weapons_new import weapons_name_to_object
from project_data.game.armors_new import armors_name_to_object
from project_data.game.magic import *
from project_data.settings.plot import get_plot, get_markup
from project_data.game.techniques import techniques_name_to_object, step_up
from project_data.game.battle_features import *

from random import randint, choice
from time import sleep


# region settings
bot = telebot.TeleBot(token=bot_token)
remove = types.ReplyKeyboardRemove()

user_d4 = [1, 2, 2, 2, 3, 3, 3, 4, 4]
enemy_d4 = [1, 1, 2, 2, 2, 3, 3, 3, 4]
user_dices = {'d4': user_d4}
enemy_dices = {'d4': enemy_d4}
# endregion
# region send
def send(message, key_plot, extra=None, key_markup=None, markup_remove=True):
    # todo: доработать картинки, гифки, видео
    id = message.from_user.id
    plot = get_plot(key=key_plot, message=message, extra=extra)
    if 'handbook' not in get_settings(id, 'special_situation') and 'speed' not in get_settings(id, 'special_situation'):
        save_settings(id, 'key_plot', key_plot)
        if key_markup: save_settings(id, 'key_markup', key_markup)

    for text in plot:
        path = 'project_data/video_and_images/'
        if text == plot[0] and markup_remove:
            if 'gif' in text:
                with open(path + text.split(';')[1], 'rb') as gif: bot.send_animation(message.chat.id, gif, reply_markup=remove)
            else: bot.send_message(message.chat.id, text, reply_markup=remove, parse_mode='HTML')
        elif text == plot[-1] and key_markup:
            bot.send_message(message.chat.id, text, reply_markup=get_markup(key=key_markup, id=id), parse_mode='HTML')
            continue
        else:
            bot.send_message(message.chat.id, text, parse_mode='HTML')
        sleep(get_settings(id, 'time_sleep'))

# endregion
# region commands
@bot.message_handler(commands=['rebirth'])
def rebirth(message):
    id = message.from_user.id
    start_over(id)
    send(message=message, key_plot='special', extra='Вы начали игру сначала. Если вы до этого сохранялись - сохранение останется.')
    send(message=message, key_plot='start', key_markup='start')


@bot.message_handler(commands=['instant_kill'])
def instant_kill(message):
    id = message.from_user.id
    if get_enemy(id, 'name'): save_enemy(id, 'health', 0)


@bot.message_handler(commands=['handbook'])
def handbook(message):
    id = message.from_user.id
    if 'handbook' not in get_settings(id, 'special_situation'):
        save_settings(id, 'special_situation', 'handbook')
    send(message=message, key_plot='pass', key_markup='handbook', markup_remove=False)

@bot.message_handler(commands=['save'])
def save(message):
    id = message.from_user.id
    if bool(get_settings(id, 'special_situation')): return
    save_all(id)
    send(message=message, key_plot='special', extra='Игра успешно сохранена.', markup_remove=False)


@bot.message_handler(commands=['load'])
def load(message):
    id = message.from_user.id
    if not get_settings(id, 'save'): return
    load_all(id)
    key_plot, key_markup = get_settings(id, 'key_plot'), get_settings(id, 'key_markup')
    send(message=message, key_plot='special', extra='Загрузка прошла успешно.')
    send(message=message, key_plot=key_plot, key_markup=key_markup)

@bot.message_handler(commands=['speed'])
def speed(message):
    id = message.from_user.id
    if 'speed' not in get_settings(id, 'special_situation'): save_settings(id, 'special_situation', 'speed')
    send(message=message, key_plot='special', extra='Введите число от 0 до 10 - это задержка между сообщениями.')
# endregion
# region fight
def fight(message):
    text = message.text
    id = message.from_user.id
    if text == 'Драться.': send(message=message, key_plot='fight start_fight', key_markup='fight roll_dice')
    elif text == 'Кинуть кубик.' and not get_fight(id, 'roll_dice'):
        send(message=message, key_plot='fight roll_dice', key_markup='fight menu', extra=self_points_before_move(id))
        save_fight(id, 'roll_dice', True)
    elif text == 'Приёмы.': send(message=message, key_plot='pass', key_markup='fight techniques_choice', markup_remove=False)
    elif text == 'Применить приём.': send(message=message, key_plot='pass', key_markup='fight techniques', markup_remove=False)
    elif text == 'Изучить свои приёмы.': send(message=message, key_plot='fight heroes_techniques', markup_remove=False)
    elif text == 'Изучить приёмы противника.': send(message=message, key_plot='fight enemies_techniques', markup_remove=False)
    elif text == 'Глубокий анализ.': send(message=message, key_plot='pass', key_markup='fight analysis', markup_remove=False)
    elif text == 'Изучить крестьянина.': send(message=message, key_plot='fight analysis', markup_remove=False, extra='self')
    elif text == 'Изучить противника.': send(message=message, key_plot='fight analysis', markup_remove=False, extra='other')
    elif text == 'Инвентарь.':
        inv = get_inventory(id, 'all')
        if inv[0] == inv[1] == inv[2] == inv[3] == '': send(message=message, key_plot='fight empty_inventory', markup_remove=False)
        else: send(message=message, key_plot='pass', key_markup='fight inventory', markup_remove=False)
    elif 'Подойти' in text:
        if get_fight(id, 'self_points') > 0 and get_fight(id, "distance") > 0:
            send(message=message, key_plot='special', markup_remove=False, extra=step_up.use(hero, id),
                 key_markup='fight techniques')
        else: send(message=message, key_plot='special', markup_remove=False, extra='Не достаточно о.п.')
    elif text == 'Закончить ход.':
        save_fight(id, '-self_sequence', '')
        self_points_after_move(id)
        save_fight(id, '+move', 1)

        send(message=message, key_plot='fight roll_dice', extra=enemy_points_before_move(id))
        actions = enemies_name_to_object[get_enemy(id, 'name')].attack(id)
        for action in actions[0]: send(message=message, key_plot='special', extra=action)
        for action in actions[1]: send(message=message, key_plot='fight enemy_t_action', extra=action)
        send(message=message, key_plot='fight result_move', key_markup='fight roll_dice')

        save_fight(id, 'roll_dice', False)
        save_fight(id, '-enemy_sequence', '')
        enemy_points_after_move(id)
        if get_hero(id, 'health') <= 0: send(message=message, key_plot='fight end')
    else:
        text = text.split('\n')[0]
        first_t, second_t, third_t, fourth_t = get_techniques(id, 'all')
        if third_t != '':
            if fourth_t != '': check_t = get_techniques(id, 'all')
            else: check_t = [first_t, second_t, third_t]
        else:
            check_t = [first_t, second_t]
        if text in check_t:
            technique = techniques_name_to_object[text]
            extra = technique.use(subject=hero, weapon=weapons_name_to_object[get_hero(id, 'equipped_weapon')], id=id)
            if extra in ['Не хватает дальности оружия.', 'Не достаточно о.п.']:
                send(message=message, key_plot='special', markup_remove=False, extra=extra)
                return
            send(message=message, key_plot='fight self_t_action', key_markup='fight techniques', extra=extra)
            if 'self' in extra:
                save_hero(id, 'health', extra[0])
                save_hero(id, 'defence', extra[1])
            else:
                save_enemy(id, 'health', extra[0])
                save_enemy(id, 'defence', extra[1])
            save_fight(id, 'distance', extra[2])
        if get_enemy(id, 'health') <= 0: send(message=message, key_plot='fight end')
# endregion
# region message_return
def message_return(message):
    id = message.from_user.id
    key_markup = get_settings(id, 'key_markup')
    if key_markup.split()[0] == 'fight':
        key_markup = key_markup.split()[1]
        if key_markup in ['techniques_choice', 'analysis']: send(message=message, key_plot='pass', key_markup='fight menu', markup_remove=False)
        elif key_markup == 'techniques': send(message=message, key_plot='pass', key_markup='fight techniques_choice', markup_remove=False)
# endregion
# region speed_special_s
def speed_special_s(message):
    text = message.text
    id = message.from_user.id
    special_situation = get_settings(id, 'special_situation')
    if text.isdigit() and 0 <= int(text) <= 10:
        save_settings(id, 'time_sleep', int(text))
        send(message=message, key_plot=get_settings(id, 'key_plot'), key_markup=get_settings(id, 'key_markup'))
        if special_situation.split(', ')[0] == 'speed': save_settings(id, '-special_situation', 'speed')
        else: save_settings(id, '-special_situation', ', speed')
# endregion
# region handbook_special_s
def handbook_special_s(message):
    text = message.text
    id = message.from_user.id
    special_situation = get_settings(id, 'special_situation')
    if text == 'Краткое обучение искусству войны.': send(message=message, key_plot='handbook training', markup_remove=False)
    elif text == 'О характеристиках.': send(message=message, key_plot='handbook guide', markup_remove=False)
    elif text == 'Вернуться.':
        key_plot, key_markup = get_settings(id, 'key_plot'), get_settings(id, 'key_markup')
        if key_plot == 'fight roll_dice': key_plot = 'pass'
        if key_plot == 'pass': markup_remove = False
        else: markup_remove = True
        send(message=message, key_plot=key_plot, key_markup=key_markup, markup_remove=markup_remove)
        if special_situation.split(', ')[0] == 'handbook': save_settings(id, '-special_situation', 'handbook')
        else: save_settings(id, '-special_situation', ', handbook')
# endregion
# region story
@bot.message_handler(commands=['start'])
def telegram_start(message):
    id = message.from_user.id
    db_reg(id)
    if get_stage(id) == 1: send(message=message, key_plot='start', key_markup='start')


@bot.message_handler(content_types=['text'])
def main(message):
    text = message.text
    id = message.from_user.id
    stage = get_stage(id)
    special_situation = get_settings(id, 'special_situation')
    choices = get_settings(id, 'choices')
    if text == 'Назад.': message_return(message)
    elif special_situation:
        if 'speed' in special_situation: speed_special_s(message)
        elif 'handbook' in special_situation: handbook_special_s(message)
        elif 'fight' in special_situation: fight(message)
    # region plot
    # region stage 1
    elif stage == 1:
        if text == 'Кто ты?':
            send(message=message, key_plot='1.1', key_markup='1.1')
        elif text == 'Какой договор?':
            send(message=message, key_plot='1.2', key_markup='1.2')
        elif text in ['Я готов.', 'Помню.']:
            send(message=message, key_plot='1.3', key_markup='1.3')
        elif text == 'Приступить к задаче.':
            send(message=message, key_plot='1.4', key_markup='1.4')
            save_stage(id, 2)
    # endregion
    # region stage 2
    elif stage == 2:
        if len(text) <= 25:
            save_hero(userid=id, param='name', val=text)
            save_stage(id, 3)
            send(message=message, key_plot='2', key_markup='2')
    # endregion
    # region stage 3
    elif 3 <= stage < 4:
        if text == 'Продолжить мечтать.':
            send(message=message, key_plot='3.1', key_markup='3.1')
        elif text == 'Попытаться вспомнить всех героев.':
            send(message=message, key_plot='3.2', key_markup='3.2')
        elif text == 'Помечтать о чём-то ещё.':
            send(message=message, key_plot='3.3', key_markup='3.3')
        elif text == 'Начать задавать вопросы.':
            send(message=message, key_plot='3.4', key_markup='3.4')
        elif text in ['Кто ты такой?', 'Ещё раз, кто ты такой?']:
            save_stage(id, get_stage(id) + 0.5)
            send(message=message, key_plot='3.4.1', key_markup='3.4.1')
        elif text in ['Я сошёл с ума?', 'Я точно не сошёл с ума?']:
            save_stage(id, get_stage(id) + 0.5)
            send(message=message, key_plot='3.4.2', key_markup='3.4.2')
        elif text in ['Как долго ты меня подслушивал?', 'Подожди, сколько уже ты здесь?']:
            save_stage(id, get_stage(id) + 0.5)
            send(message=message, key_plot='3.4.3', key_markup='3.4.3')
    # endregion
    # region stage 4
    elif stage == 4:
        if text in ['Кто ты такой?', 'Ещё раз, кто ты такой?', 'Я сошёл с ума?', 'Я точно не сошёл с ума?',
                    'Как долго ты меня подслушивал?', 'Подожди, сколько уже ты здесь?']:
            send(message=message, key_plot='4.1', key_markup='4.1')
        elif text == 'Попытаться всё осознать.':
            send(message=message, key_plot='4.2', key_markup='4.2')
        elif text == 'Спуститься со скалы.':
            send(message=message, key_plot='4.3', key_markup='4.3')
        elif text == 'Пойти вперёд.':
            send(message=message, key_plot='4.4', key_markup='4.4')
        elif text == 'Продолжить путь.':
            send(message=message, key_plot='4.5', key_markup='4.5')
        elif text == 'Подойти к группе крестьянок.':
            send(message=message, key_plot='4.6', key_markup='4.6')
        elif text == 'Понаблюдать за странной парочкой.':
            send(message=message, key_plot='4.7', key_markup='4.7')
        elif text == 'Пойти в сторону бабки.':
            send(message=message, key_plot='4.8', key_markup='4.8')
            save_settings(id, 'choices', '4:1')
            save_stage(id, 5)
        elif text == 'Пойти прочь от странной парочки.':
            send(message=message, key_plot='4.9', key_markup='4.9')
            save_settings(id, '-reputation_storyteller', 1)
        elif text in ['Пойти в сторону крестьянок.', 'Трус.']:
            send(message=message, key_plot='4.10', key_markup='4.10', extra=text)
            save_settings(id, 'choices', '4:2')
            save_stage(id, 5)
            # todo: доделать
    # endregion
    # region stage 5
    elif stage == 5:
       if text == 'Бежать за ними.':
           send(message=message, key_plot='5.1', key_markup='5.1')
       elif text == 'Вмешаться.':
           send(message=message, key_plot='5.2', key_markup='fight start')
           save_settings(id, 'special_situation', 'fight')
    # endregion
    # endregion
# endregion
bot.infinity_polling()
