from project_data.settings.fonts import *
from project_data.db_birth_hero.db_operation import *
from project_data.game.enemies import enemies_name_to_object, hero
from project_data.game.techniques import techniques_name_to_object
from project_data.game.weapons_new import weapons_name_to_object
from project_data.game.armors_new import armors_name_to_object

from telebot import types
from random import choice


Button = types.KeyboardButton
Markup = types.ReplyKeyboardMarkup
void = underlined('Тенебрис')
voice = underlined('Голос')
unknown = underlined('???')
story_teller = underlined('Сказочник')
narrator = underlined('Рассказчик')
grandma = underlined('Бабка')
rogue = underlined('Разбойник')
grandma_with_name = underlined('Бабка (Преведа)')
rogue_with_name = underlined('Разбойник (Алчек)')


def fight(message, key, extra):
    id = message.from_user.id
    name_in_text = get_hero(id, "name")
    # region start_fight
    if key == 'start_fight':
        if get_stage(id) == 5:
            text = [
                bold('Совет от разработчиков: если ты играешь впервые, то стоит ознакомится со справочником.'),
                bold('Для этого необходимо ввести "/handbook" и выбрать нужный раздел.')
            ]
        else:
            text = [
                bold('Время боя.'),
                bold('А значит твой кубик снова твой лучший друг.')
            ]
    # endregion
    # region roll_dice
    elif key == 'roll_dice':
        points = extra[-1]
        special = extra[1]
        if 'self' in extra:
            text = [bold(f'Ход {get_fight(id, "move")}')]
            if special and not str(special).isdigit():
                text.append(bold(f'{get_hero(id, "name")} использовал особенность "{special}."'))
            else:
                text.append(bold('Ты ожидаешь вердикт кубика судьбы.'))
            text.append(bold(f'Герою выпало {points} о.п.'))
            if get_fight(id, 'self_points') == 0:
                save_fight(id, 'self_points', points)
            else:
                save_fight(id, '+self_points', points)
                text.append(bold(f'Теперь у него {get_fight(id, "self_points")} о.п.'))
        else:
            if special: text = [bold(f'{get_enemy(id, "name")} использовал особенность "{special}."')]
            else: text = list()
            text.append(bold(f'Противнику выпало {points} о.п.'))
            if get_fight(id, 'enemy_points') == 0: save_fight(id, 'enemy_points', points)
            else:
                save_fight(id, '+enemy_points', points)
                text.append(bold(f'Теперь у него {get_fight(id, "enemy_points")} о.п.'))
    # endregion
    # region heroes_techniques
    elif key == 'heroes_techniques':
        first, second, third, fourth = get_techniques(id, 'all')
        first = techniques_name_to_object[first]
        second = techniques_name_to_object[second]
        text = [
            bold(f'1) {first.name}: стоимость {first.cost} о.п. Механика: {first.mechanics}'),
            bold(f'2) {second.name}: стоимость {second.cost} о.п. Механика: {second.mechanics}')
        ]
        if third != '—':
            third = techniques_name_to_object[third]
            text.append(bold(f'3) {third.name}: стоимость {third.cost} о.п. Механика: {third.mechanics}'))
        if fourth != '—':
            fourth = techniques_name_to_object[fourth]
            text.append(bold(f'4) {fourth.name}: стоимость {fourth.cost} о.п. Механика: {fourth.mechanics}'))
    # endregion
    # region enemies_techniques
    elif key == 'enemies_techniques':
        first, second, third, fourth = enemies_name_to_object[get_enemy(id, 'name')].techniques
        text = [
            bold(f'1) {first.name}: стоимость {first.cost} о.п. Механика: {first.mechanics}'),
            bold(f'2) {second.name}: стоимость {second.cost} о.п. Механика: {second.mechanics}')
        ]
        if third: text.append(bold(f'3) {third.name}: стоимость {third.cost} о.п. Механика: {third.mechanics}'))
        if fourth: text.append(bold(f'4) {fourth.name}: стоимость {fourth.cost} о.п. Механика: {fourth.mechanics}'))
    # endregion
    # region empty_inventory
    elif key == 'empty_inventory':
        text = [
            bold('Ты хочешь использовать вещи из инвентаря, дабы облегчить бой.'),
            bold('Но он пуст.')]
    # endregion
    # region self_t_action
    elif key == 'self_t_action':
        new_health, new_defence, new_distance, actor, t_name = extra
        distance = new_distance - get_fight(id, 'distance')
        text = [bold(f'{name_in_text} использовал технику *{t_name}*.')]
        enemy = enemies_name_to_object[get_enemy(id, 'name')]
        if actor == 'self':
            health, defence = new_health - get_hero(id, 'health'), new_defence - get_hero(id, 'defence')
            if health > 0: text.append(bold(f'Он увеличил своё здоровье на {health}.'))
            if defence > 0: text.append(bold(f'Он увеличил свою защиту на {defence}.'))
            text.append(
                bold(f'Итог для {name_in_text}:\n'
                     f'Здоровье: {new_health}/{get_hero(id, "max_health")}\n'
                     f'Защита: {new_defence}/{get_hero(id, "max_defence")}\n'))
        else:
            health, defence = get_enemy(id, 'health') - new_health, get_enemy(id, 'defence') - new_defence
            if health > 0: text.append(bold(f'Он снёс противнику {health} единиц здоровья.'))
            if defence > 0: text.append(bold(f'Он снёс противнику {defence} единиц защиты.'))
            text.append(
                bold(f'Итог для {get_enemy(id, "name")}:\n'
                     f'Здоровье: {new_health}/{enemy.health}\n'
                     f'Защита: {new_defence}/{enemy.defence}\n'))
        if distance > 0: text.append(bold(f'Он увеличил дистанцию на {distance}.'))
        elif distance < 0: text.append(bold(f'Он сократил от противника на {distance}'))
        text.append(bold(f'Дистанция: {new_distance}.'))
        text.append(bold(f'Осталось {get_fight(id, "self_points")} о.п.'))
        save_fight(id, 'distance', new_distance)
    # endregion
    # region enemy_t_action
    elif key == 'enemy_t_action':
        if 'pass' in extra: return [bold(f'{get_enemy(id, "name")} решил пропустить ход.')]
        health, defence, distance, actor, t_name = extra
        text = [
            bold(f'{get_enemy(id, "name")} использовал технику *{t_name}*.')
        ]
        if actor == 'self':
            if health > 0: text.append(bold(f'Он увеличил своё здоровье на {health}.'))
            if defence > 0: text.append(bold(f'Он увеличил свою защиту на {defence}.'))
        else:
            if health > 0: text.append(bold(f'Он снёс герою {health} единиц здоровья.'))
            if defence > 0: text.append(bold(f'Он снёс герою {defence} единиц защиты.'))
        if distance > 0: text.append(bold(f'Он увеличил дистанцию на {distance}.'))
        elif distance < 0: text.append(bold(f'Он сократил от противника на {distance}'))
    # endregion
    # region result_move
    elif key == 'result_move':
        enemy = enemies_name_to_object[get_enemy(id, 'name')]
        text = [
            bold(f'Итог для {name_in_text}:\n'
                 f'Здоровье: {get_hero(id, "health")}/{get_hero(id, "max_health")}\n'
                 f'Защита: {get_hero(id, "defence")}/{get_hero(id, "max_defence")}\n'),
            bold(f'Итог для {enemy.name}:\n'
                 f'Здоровье: {get_enemy(id, "health")}/{enemy.health}\n'
                 f'Защита: {get_enemy(id, "defence")}/{enemy.defence}\n'),
            bold(f'Дистанция: {get_fight(id, "distance")}.')
        ]
    # endregion
    # region analysis
    elif key == 'analysis':
        if extra == 'self':
            text = [
                bold(f'Имя: {get_hero(id, "name")}.'),
                bold(f'Мастерство: {get_hero(id, "battle_level")} ур.')
            ]
            magic = get_hero(id, 'magic_level')
            if magic > 0: text.append(bold(f'Могущество: {magic} ур.'))
            weapon = weapons_name_to_object[get_hero(id, "equipped_weapon")]
            text.append(bold(
                f'Об оружие. Название: {weapon.name}; дальность: {weapon.w_range}; обычный урон: {weapon.damage}.'))
            armor = armors_name_to_object[get_hero(id, "equipped_armor")]
            text.append(
                bold(f'О броне. Название: {armor.name}; защита: {armor.defence}; особенность: {armor.special.name}.'))
            text.append(bold(f'Особенность: {armor.special.mechanics}'))
            text.append(bold(f'История: {hero.description}.'))
        else:
            enemy = enemies_name_to_object[get_enemy(id, 'name')]
            text = [bold(f'Имя: {enemy.name}.')]
            weapon = enemy.weapon
            text.append(bold(
                f'Об оружие. Название: {weapon.name}; дальность: {weapon.w_range}; обычный урон: {weapon.damage}.'))
            armor = enemy.armor
            text.append(
                bold(f'О броне. Название: {armor.name}; защита: {armor.defence}; особенность: {armor.special.name}.'))
            text.append(bold(f'Особенность: {armor.special.mechanics}'))
            text.append(bold(f'История: {enemy.description}.'))
    # endregion
    elif key == 'end':
        text = ['Спасибо за игру. Конец демо!']
    return text

def handbook(key):
    # region training
    if key == 'training':
        text = [
            bold('Как проходят бои.'),
            bold('1) В начале своего хода ты бросаешь кубик (стартовый кубик - d4).'),
            bold('Выпавшее на кубике значение = очкам потенциала или же "о.п.".'),
            bold('2) О.п. можно использовать для применения различных приёмов для нанесения урона или собственной защиты.'),
            bold('3) После того, как ты сделал, что хотел, ты нажимаешь "закончить ход.".'),
            bold('4) Дальше начинается ход противника. Его ход проходит по аналогичному принципу.'),
            bold('5) Проигрывает тот, у кого здоровье упало ниже 0.')]
    # endregion
    # region guide
    elif key == 'guide':
        text = [
            bold('1) Одни из главных показателей - здоровье и защита.'),
            bold('Здоровье - это то, что позволяет тебе жить. Если оно опустится до 0 - ты проиграл бой.'),
            bold('Защита это почти то же самое, что и здоровье, но она восстанавливается после боя и она зависит от надетой брони.'),
            bold('2) Дистанция показывает, на каком расстояние ты находишься от противника. 0 дистанция - самая ближняя.'),
            bold('Разное оружие может атаковать на разной дистанции.'),
            bold('3) Урон оружия - обычный урон; специальный урон - тот урон, который даёт ваше действие.'),
            bold('4) Использование чего-либо в бою - действие.')]
    # endregion
    return text
def get_plot(message, key, extra):
    id = message.from_user.id
    name = underlined(get_hero(id, "name"))
    name_in_text = get_hero(id, "name")
    # region pass
    if key == 'pass': text = ['...']
    # endregion
    # region special
    elif key == 'special': text = [bold(extra)]
    # endregion
    # region special_situations
    # region fight
    elif key.split()[0] == 'fight':
        key = key.split()[1]
        text = fight(message, key, extra)
    # endregion
    # region handbook
    elif key.split()[0] == 'handbook':
        key = key.split()[1]
        text = handbook(key)
    # endregion
    # endregion
    # region plot
    # region start
    elif key == 'start':
        text = [
            'gif;start.mp4',
            ancient_language(f"{void}: Вновь приветствую тебя, соскучился?"),
            ancient_language(f"{void}: Надеюсь, ты помнишь наш договор?")
        ]
    # endregion
    # region stage 1
    elif key[0] == '1':
        if key == '1.1':
            text = [
                italics(f"{unknown}: Кто ты?"),
                ancient_language(f"{void}: Ох, не уж то ты меня не помнишь?"),
                ancient_language(f"{void}: Ах, как жаль."),
                ancient_language(f"{void}: Я та, благодаря кому ты до сих пор жив.")]
        elif key == '1.2':
            text = [
                italics(f"{unknown}: Что я должен?"),
                ancient_language(f"{void}: Душка, ты должен убить короля."),
                ancient_language(f"{void}: И тогда ты получишь свою награду сполна."),
                ancient_language(f"{void}: Я уж сдержу своё слово, а ты?")]
        elif key == '1.3':
            text = [
                italics(f"{unknown}: Достаточно болтовни."),
                ancient_language(f"{void}: Как скажешь."),
                ancient_language(f"{void}: Удачи же тебе."),
                ancient_language(f"{void}: Надеюсь, ты сможешь решить вопрос со своим крестьянином.")]
        elif key == '1.4':
            text = [
                bold('Для того, чтобы сохраниться введите "/save", чтобы загрузиться - "/load"'),
                bold('За раз возможно только одно сохранение, нельзя сохраняться во время событий (бой, справочник и т.п.).'),
                bold('Чтобы начать игру сначала введите "/rebirth".'),
                bold('Настроить задержку между сообщениями -  "/speed".'),
                bold('Как же будут звать твоего крестьянина?'),
                bold('Необходимо ввести имя для крестьянина (не больше 25 символов).')]
    # endregion
    # region stage 2
    elif key == '2':
        text = [
            italics(f'Спустя лишь миг ты видишь молодого крестьянина, задумчиво смотрящего в сторону замка.'),
            italics(f'Ты чувствуешь, что этот мечтатель не создаст проблем.'),
            italics(f'Теперь, вы одно целое.'),
            italics(f'Всё зависит только от тебя.'),
            f'{name}: Эх, как же величественен наш замок. Хотел бы и я там жить.',
            f'{name}: Не, наша деревня хороша, конечно. Но жить в центре величайшего королевства, в окружении доблестных защитников и настоящего героя...',
            f'{name}: Жаль, что это лишь мечта.',
            f'{name}: Ну не, меня когда-нибудь обязательно заметят.',
            f'{name}: Говорят же, как даже крестьян звали жить туда. Хоть и давно такого не было.',
            f'{name}: Авось, и мне подвернётся какой-нибудь случай, и я смогу проявить себя.',
            f'{name}: Да, так и будет.']
    # endregion
    # region stage 3
    elif key[0] == '3':
        if key == '3.1':
            text = [
                f'{name}: Интересно, а были ли среди героев обычные крестьяне?',
                f'{name}: Хм.']
        elif key == '3.2':
            text = [
                f'{name}: Так...',

                f'{name}: Наш король, его отец, кто ещё?',

                f'{name}: Так, отец его отца, ну и основатель Регнум Радиантем...',

                f'{name}: Странно, неужели герои - это одна династия избранных?',

                f'{name}: А у других народов были герои?',

                f'{name}: Надо будет задать все эти вопросы старосте. Да, это хорошая идея.'
            ]
        elif key == '3.3':
            text = [
                f'{name}: Ну как же притягателен образ крестьянина-героя...',

                f'{name}: Но у всех героев есть наставник, сияющие доспехи и легендарное оружие...',

                f'{voice}: Хороша мысль, крестьянин-герой.',

                f'{name}: Кто здесь?!',
                # Рассказчик появляется в виде тени
                f'{story_teller}: Не бойся, я - Сказочник.',

                f'{story_teller}: Я тут уже некоторое время тебя слушаю и всё пытаюсь понять, что происходит.',

                f'{story_teller}: Послушав тебя, кажется я понял, зачем я здесь.',
            ]
        elif key == '3.4':
            text = [
                f'{name}: Ох, у меня так много вопросов...',

                f'{name}: С чего бы начать...'
            ]
        elif key == '3.4.1':
            text = [
                f'{name}: Ты кто или что такое?',

                f'{story_teller}: Мне самому не совсем понятно.',

                f'{story_teller}: Всё что я знал, я рассказал тебе.',

                f'{story_teller}: Дальше уж разберёмся.',
            ]
        elif key == '3.4.2':
            text = [
                f'{name}: Мне это ведь только кажется, да ведь?',

                f'{story_teller}: Я в этом сомневаюсь, так что можешь расслабиться.',

                f'{story_teller}: Думаю, у тебя будет возможность убедиться во всём самому.',

                f'{story_teller}: А вообще, странно, что ты задаёшь этот вопрос мне.'
            ]
        elif key == '3.4.3':
            text = [
                f'{name}: И как долго ты здесь?',

                f'{story_teller}: Сложно сказать, сначала я был больше поглощён своими мыслями.',

                f'{story_teller}: Ну, а так где-то с рассуждения о королях я тебя слушал.'
            ]
    # endregion
    # region stage 4
    elif key[0] == '4':
        if key == '4.1':
            text = [
                f'{story_teller}: Я понял, вопросов у тебя много, но давай перейдём ближе к делу.',

                f'{story_teller}: Во-первых, я понял, что часть моих магических способностей осталась со мной.',

                f'{story_teller}: Правда почти всё уходит на общение с тобой и поддержание этого облика.',

                f'{story_teller}: Во-вторых, я оказался в моменте, где ты думаешь о том, чтобы примерить образ героя.',

                f'{story_teller}: А я могу тебе с этим помочь.',

                f'Ты видишь, как Сказочник делает вид, что щёлкает пальцами (а может для него это и по-настоящему).',

                f'Мгновеньем позже на герое появляются блестящие доспехи и героического вида меч.'
            ]
        elif key == '4.2':
            text = [
                f'{name}: Ух ты!',

                f'{name}: Да это же, да как это!',

                f'{name}: Ваааау...',

                f'{story_teller}: Ха, рад, что тебе понравилось.',

                f'{story_teller}: Но на это у меня ушло довольно много сил.',

                f'{story_teller}: Так что ближайшее время я буду просто голосом в твоей голове.',

                f'{story_teller}: Пойдём, поищем приключений, герой.',

                f'После этого, тень, именуемая сказочником, испаряется в воздухе.'
            ]
        elif key == '4.3':
            text = [
                f'{name}: Даа, жизнь кипит, как всегда.',

                f'{story_teller}: Сейчас начало дня, думаю это оправдано.',

                f'{name}: И то правда.'
            ]
        elif key == '4.4':
            text = [
                f'{name}: Сказочник?',

                f'{story_teller}: Что случилось?',

                f'{name}: Почему люди так странно на меня смотрят?',

                f'{story_teller}: Может потому что ты облачён в шикарный доспех?',

                f'{name}: А, думаю в этом есть смысл.'
            ]
        elif key == '4.5':
            text = [
                f'{name}: Как ты думаешь, наше приключение может немного подождать?',

                f'{story_teller}: А что случилось?',

                f'{name}: Да там подруги моей возлюбленной, обычно они просто подшучивали надо мной и дальше дело не шло.',

                f'{name}: А сейчас я смогу произвести впечатление.',

                f'{story_teller}: Я только одного не понимаю.',

                f'{story_teller}: Если у тебя есть возлюбленная, то зачем производить впечатление на её подруг?',

                f'{name}: Мне друг говорил, что это самый действенный и надёжный способ.',

                f'{story_teller}: А он как раз мастер в этом, да?',

                f'{name}: Я знал, что ты поймёшь!',

                f'{story_teller}: Ай ладно, иди к ним.',

                f'{story_teller}: Всё равно пока у нас нет какой-то цели.',

                f'{name}: Спасибо!',

                f'{story_teller}: Иди уже.'
            ]
        elif key == '4.6':
            text = [
                f'Ты видишь, как мужичок странной походной подходит к тётке.',

                f'{name}: Мне кажется или тот мужик себя странно ведёт?',

                f'{story_teller}: О чём ты?',

                f'{name}: Вот что ему могло понадобится от той бабки?',

                f'{story_teller}: Мне кажется, ты не о том думаешь сейчас.',

                f'{story_teller}: Там подруги твоей пассии.',

                f'{story_teller}: Это ещё пару секунд назад для тебя много значило.',

                f'{name}: А вдруг что-то серьёзное?',

                f'{story_teller}: Хорошо, можем постоять и посмотреть.'
            ]
        elif key == '4.7':
            text = [
                f'{name}: А вот теперь это явно напоминает спор.',

                f'{story_teller}: Так иди проверь.'
            ]
        elif key == '4.8':
            text = [
                'Ты видишь как бабка отталкивает от себя странного гражданина и убегает.',

                f'{name}: Кажется пора ускориться!'
            ]
        elif key == '4.9':
            text = [
                italics(f'Ты ощущаешь страх, испытываемый {name_in_text}.'),

                f'{name}: У них точно всё хорошо.',

                f'{story_teller}: Ну, допустим.',

                f'{story_teller}: Я надеялся, что ты хоть проверишь это.',

                bold(f'Сказочник не оценил поступок.')
            ]
        elif key == '4.10':
            if extra == 'Трус.': text = [italics(f'{unknown}: Трус.')]
            else: text = list()
            text.append(f'Продолжение следует...')
            text.append(f'Конец демо!')

    # endregion
    # region stage 5
    elif key[0] == '5':
        if key == '5.1':
            text = [
                'Твоему взору предстала сцена: разбойник, словно хищник, встретивший добычу, приближался к бабушке.',

                f'{rogue}: Так значит вот на кого ты меня променяла?',

                f'{rogue}: На соплячку?!',

                f'{grandma}: Ты сам выбрал такой путь, Алчек.',

                f'{grandma}: Ты знал к чему это приведёт.',

                f'{rogue_with_name}: Наша таверна нуждалась в деньгах и где я не прав?',

                f'{grandma}: Как ты заметил, таверна пережила войну и без твоих денег.',

                f'{grandma}: И она также прекрасна для горожан как раньше и без тебя.',

                f'{rogue_with_name}: Я пошёл по-этому пути для нас!',

                f'{rogue_with_name}: А тебе нужен был лишь повод, чтобы натравить на меня стражу и выкинуть на улицу ни с чем!'
            ]
        elif key == '5.2':
            text = [
                f'{name}: А ну ка! Что здесь происходит?',

                f'{rogue_with_name}: О добрый самаритянин, а не пойти бы тебе прочь отсюда?',

                f'{name}: А может это ты пойдёшь отсюда вон?',

                f'{rogue_with_name}: Ой, а я и не думал, что у стражи так подвешен язык.',

                f'{rogue_with_name}: А, теперь-то я вижу. Ты жалкий новобранец, пытающийся строить из себя героя.',

                f'{rogue_with_name}: Ну что ж, сейчас я преподам тебе жизненный урок.',

                f'{rogue_with_name}: Или просто убью.',

                italics('Ты чувствуешь: драки не избежать.')
            ]
    # endregion
    # endregion
    return text


def get_markup(key, id=None):
    markup = Markup(resize_keyboard=True)
    # region special_situations
    # region fight
    if key.split()[0] == 'fight':
        key = key.split()[1]
        if key == 'start':
            first = Button('Драться.')
            markup.add(first)
        elif key == 'roll_dice':
            first = Button('Кинуть кубик.')
            markup.add(first)
        elif key == 'menu':
            first = Button('Приёмы.')
            second = Button('Магия.')
            third = Button('Инвентарь.')
            fourth = Button('Глубокий анализ.')
            fifth = Button('Закончить ход.')
            if get_hero(id, 'magic_level') > 0:
                markup.add(first, second)
            else:
                markup.add(first)
            markup.add(third, fourth)
            markup.add(fifth)
        elif key == 'techniques_choice':
            first = Button('Применить приём.')
            second = Button('Изучить свои приёмы.')
            third = Button('Изучить приёмы противника.')
            fourth = Button('Назад.')
            markup.add(first)
            markup.add(second, third)
            markup.add(fourth)
        elif key == 'techniques':
            first, second, third, fourth = get_techniques(id, 'all')
            first = techniques_name_to_object[first]
            second = techniques_name_to_object[second]

            first = Button(f'{first.name}\n{first.cost} о.п.')
            second = Button(f'{second.name}\n{second.cost} о.п.')

            if third != '—':
                third = Button(f'{third.name}\n{third.cost} о.п.')
            else:
                third = Button(third)

            if fourth != '—':
                fourth = Button(f'{fourth.name}\n{fourth.cost} о.п.')
            else:
                fourth = Button(fourth)

            fifth = Button('Подойти\n1 о.п. ')
            sixth = Button('Назад.')
            markup.add(first, second)
            markup.add(third, fourth)
            if get_fight(id, 'distance') > 0: markup.add(fifth, sixth)
            else: markup.add(sixth)
        elif key == 'analysis':
            first = Button('Изучить крестьянина.')
            second = Button('Изучить противника.')
            third = Button('Назад.')
            markup.add(first, second)
            markup.add(third)
        elif key == 'inventory':
            pass
            # todo: доделать
    # endregion
    # region handbook
    elif key == 'handbook':
        first = Button('Краткое обучение искусству войны.')
        second = Button('О характеристиках.')
        third = Button('Вернуться.')
        markup.add(first)
        markup.add(second, third)
    # endregion
    # endregion
    # region plot
    # region start
    elif key == 'start':
        first = Button('Кто ты?')
        second = Button('Какой договор?')
        third = Button('Помню.')
        markup.add(first, second)
        markup.add(third)
    # endregion
    # region stage 1
    elif key[0] == '1':
        if key == '1.1':
            first = Button('Какой договор?')
            second = Button('Я готов.')
            markup.add(first)
            markup.add(second)
        elif key == '1.2':
            first = Button('Кто ты?')
            second = Button('Я готов.')
            markup.add(first)
            markup.add(second)
        elif key == '1.3':
            first = Button('Приступить к задаче.')
            markup.add(first)
        elif key == '1.4':
            save_1 = get_settings(id, 'save_1')
            save_2 = get_settings(id, 'save_2')
            save_3 = get_settings(id, 'save_3')
            if save_1 != '' or save_2 != '' or save_3 != '':
                second = Button('Вернуться к одному из моментов.')
                markup.add(second)
    # endregion
    # region stage 2
    elif key == '2':
        first = Button('Продолжить мечтать.')
        markup.add(first)
    # endregion
    # region stage 3
    if key[0] == '3':
        if key == '3.1':
            first = Button('Попытаться вспомнить всех героев.')
            markup.add(first)
        elif key == '3.2':
            first = Button('Помечтать о чём-то ещё.')
            markup.add(first)
        elif key == '3.3':
            first = Button('Начать задавать вопросы.')
            markup.add(first)
        elif '3.4' in key:
            if key != '3.4.1':
                first = Button('Кто ты такой?')
            else:
                first = Button('Ещё раз, кто ты такой?')
            if key != '3.4.2':
                second = Button('Я сошёл с ума?')
            else:
                second = Button('Я точно не сошёл с ума?')
            if key != '3.4.3':
                third = Button('Как долго ты меня подслушивал?')
            else:
                third = Button('Подожди, сколько уже ты здесь?')
            markup.add(first, second)
            markup.add(third)
    # endregion
    # region stage 4
    if key[0] == '4':
        if key == '4.1':
            first = Button('Попытаться всё осознать.')
            markup.add(first)
        elif key == '4.2':
            first = Button('Спуститься со скалы.')
            markup.add(first)
        elif key == '4.3':
            first = Button('Пойти вперёд.')
            markup.add(first)
        elif key == '4.4':
            first = Button('Продолжить путь.')
            markup.add(first)
        elif key == '4.5':
            first = Button('Подойти к группе крестьянок.')
            markup.add(first)
        elif key == '4.6':
            first = Button('Понаблюдать за странной парочкой.')
            second = Button('Пойти в сторону бабки.')
            third = Button('Пойти в сторону крестьянок.')
            markup.add(first)
            markup.add(second, third)
        elif key == '4.7':
            first = Button('Пойти в сторону бабки.')
            second = Button('Пойти прочь от странной парочки.')
            markup.add(first, second)
        elif key == '4.8':
            first = Button('Бежать за ними.')
            markup.add(first)
        elif key == '4.9':
            first = Button('Трус.')
            markup.add(first)
    # endregion
    # region stage 5
    if key[0] == '5':
        if key == '5.1':
            first = Button('Вмешаться.')
            markup.add(first)
    # endregion
    # endregion
    return markup