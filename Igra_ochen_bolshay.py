import random
import os
from datetime import datetime

sd = int(input('Введи seed для рандомайзера: '))
random.seed(sd)

class GameState:
    """Класс для сохранения состояния игры в txt файлах"""
    def __init__(self):
        self.saves_dir = "game_saves"
        self.current_save = None
        
        # Создаем папку для сохранений, если ее нет
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
    
    def save_game(self, player_name, team, artifacts, story_branch, chapter, outcome):
        """Сохраняем игру в txt файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"{self.saves_dir}/{player_name}_{timestamp}.txt"
        
        save_data = f"""=== СОХРАНЕНИЕ ИГРЫ ===
Дата: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Игрок: {player_name}
Ветка сюжета: {self._get_branch_name(story_branch)}
Глава: {chapter}
Результат: {outcome}
Seed: {sd}

=== КОМАНДА ===
"""
        # Информация о команде
        for i, char in enumerate(team, 1):
            save_data += f"{i}. {char.name} ({char.char_type})\n"
            save_data += f"   HP: {char.hp}/{char.max_hp}, MP: {char.mp}/{char.max_mp}\n"
            save_data += f"   Сила: {char.strength}, Ловкость: {char.agility}, Интеллект: {char.intellect}\n"
            save_data += f"   Артефакты: {len(char.artifacts)}\n"
            for artifact in char.artifacts:
                save_data += f"   - {artifact['name']}: {artifact['description']}\n"
            save_data += "\n"
        
        # Информация о найденных артефактах
        save_data += "=== НАЙДЕННЫЕ АРТЕФАКТЫ ===\n"
        for i, artifact in enumerate(artifacts, 1):
            save_data += f"{i}. {artifact['name']}\n"
            save_data += f"   Тип: {artifact['type']}\n"
            save_data += f"   Эффект: {artifact['description']}\n\n"
        
        save_data += f"=== СТАТУС ===\nИгра сохранена успешно!\n"
        
        # Записываем в файл
        with open(save_filename, 'w', encoding='utf-8') as f:
            f.write(save_data)
        
        # Также добавляем запись в общий лог
        self._add_to_log(player_name, story_branch, chapter, outcome)
        
        self.current_save = save_filename
        print(f"\n=== Игра сохранена в файле: {save_filename} ===")
        
        return save_filename
    
    def _get_branch_name(self, branch_num):
        """Получаем название ветки по номеру"""
        branches = {
            1: "Путь Воина",
            2: "Путь Мага",
            3: "Путь Искателя"
        }
        return branches.get(branch_num, "Неизвестная ветка")
    
    def _add_to_log(self, player_name, story_branch, chapter, outcome):
        """Добавляем запись в общий лог игры"""
        log_file = "game_log.txt"
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Игрок: {player_name} | Ветка: {self._get_branch_name(story_branch)} | Глава: {chapter} | Результат: {outcome}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def load_saves_list(self):
        """Загружаем список всех сохранений"""
        saves = []
        if os.path.exists(self.saves_dir):
            for filename in os.listdir(self.saves_dir):
                if filename.endswith('.txt'):
                    filepath = os.path.join(self.saves_dir, filename)
                    try:
                        # Читаем первую строку для быстрой информации
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            if len(lines) > 2:
                                # Извлекаем информацию из файла
                                player_name = lines[2].split(": ")[1].strip()
                                date_time = lines[1].split(": ")[1].strip()
                                branch = lines[3].split(": ")[1].strip()
                                
                                saves.append({
                                    'filename': filename,
                                    'filepath': filepath,
                                    'player_name': player_name,
                                    'date': date_time,
                                    'branch': branch
                                })
                    except:
                        continue
        return saves
    
    def show_saves(self):
        """Показываем список сохранений"""
        saves = self.load_saves_list()
        
        if not saves:
            print("\nНет сохраненных игр")
            return

        print("\nСОХРАНЕНИЯ:\n")
        
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save['player_name']}")
            print(f"   Дата: {save['date']}")
            print(f"   Ветка: {save['branch']}")
            print(f"   Файл: {save['filename']}")
            print()
    
    def load_save(self, save_index):
        """Загружаем конкретное сохранение"""
        saves = self.load_saves_list()
        
        if 0 <= save_index < len(saves):
            save_file = saves[save_index]['filepath']
            print(f"\nЗагружаем сохранение из: {save_file}")
            
            # Читаем и показываем информацию о сохранении
            with open(save_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\nИНФОРМАЦИЯ О СОХРАНЕНИИ:\n")
                
                # Выводим только первую часть файла (до артефактов)
                lines = content.split('\n')
                for i in range(min(10, len(lines))):  # Первые 10 строк
                    print(lines[i])
                
                print("\n... (полную информацию смотрите в файле сохранения)")
            
            return saves[save_index]
        else:
            print("Неверный номер сохранения")
            return None
    
    def show_statistics(self):
        """Показываем статистику из лога"""
        if os.path.exists("game_log.txt"):
            print("\nСТАТИСТИКА ИГР:\n")
            
            with open("game_log.txt", 'r', encoding='utf-8') as f:
                games = f.readlines()
            
            if games:
                total_games = len(games)
                victories = sum(1 for game in games if "победа" in game.lower() or "complete_victory" in game)
                defeats = sum(1 for game in games if "поражение" in game.lower() or "defeat" in game)
                
                print(f"Всего игр сыграно: {total_games}")
                print(f"Побед: {victories}")
                print(f"Поражений: {defeats}")
                print(f"Процент побед: {victories/total_games*100:.1f}%" if total_games > 0 else "Процент побед: 0%")
                
                # Статистика по веткам
                branches = {"Путь Воина": 0, "Путь Мага": 0, "Путь Искателя": 0}
                for game in games:
                    for branch in branches:
                        if branch in game:
                            branches[branch] += 1
                
                print("\nПо веткам сюжета:")
                for branch, count in branches.items():
                    print(f"  {branch}: {count}")
            else:
                print("Еще нет сыгранных игр")
        else:
            print("Файл статистики не найден")

class Character:
    """Базовый класс персонажа"""
    def __init__(self, name, char_type, hp=100, mp=100, strength=50, agility=50, intellect=50, damage=50):
        self.name = name
        self.char_type = char_type
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.strength = strength
        self.agility = agility
        self.intellect = intellect
        self.damage = damage
        self.artifacts = []
        self.level = 1
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def restore_mp(self, amount):
        self.mp += amount
        if self.mp > self.max_mp:
            self.mp = self.max_mp
    
    def attack(self, target):
        dam = (self.strength * 0.8) + (self.damage * 0.6) + (self.intellect * 0.5)
        dam_random = random.randint(1, int(dam))
        
        # Проверяем артефакты для усиления атаки
        for artifact in self.artifacts:
            if artifact.get('type') == 'attack_boost':
                dam_random = int(dam_random * (1 + artifact['value']))
        
        target.take_damage(dam_random)
        self.mp -= 10
        return dam_random
    
    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        
        # Применяем эффекты артефакта
        if artifact['type'] == 'hp_boost':
            self.max_hp = int(self.max_hp * (1 + artifact['value']))
            self.hp = int(self.hp * (1 + artifact['value']))
        elif artifact['type'] == 'strength_boost':
            self.strength = int(self.strength * (1 + artifact['value']))
        elif artifact['type'] == 'agility_boost':
            self.agility = int(self.agility * (1 + artifact['value']))
        elif artifact['type'] == 'intellect_boost':
            self.intellect = int(self.intellect * (1 + artifact['value']))
    
    @property
    def is_alive(self):
        return self.hp > 0
    
    @property
    def has_mp(self):
        return self.mp > 0
    
    def __str__(self):
        return f"{self.name} ({self.char_type}): HP={self.hp}/{self.max_hp}, MP={self.mp}/{self.max_mp}"

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, "Воин", hp=150, mp=80, strength=100, agility=30, intellect=20, damage=70)
    
    def war_attack(self, target):
        dam = (self.strength * 0.9) + (self.damage * 0.6)
        dam_random = random.randint(1, int(dam))
        
        for artifact in self.artifacts:
            if artifact.get('type') == 'attack_boost':
                dam_random = int(dam_random * (1 + artifact['value']))
        
        target.take_damage(dam_random)
        self.mp -= 15
        
        # Шанс на двойной удар
        if random.random() < 0.4:  # 40% шанс
            bonus_damage = int(dam_random * 0.5)
            target.take_damage(bonus_damage)
            print(f"✨ {self.name} совершает двойной удар! Дополнительный урон: {bonus_damage}")
            return dam_random + bonus_damage
        
        return dam_random

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, "Маг", hp=100, mp=200, strength=20, agility=50, intellect=100, damage=30)
        self.mana = 100
    
    def magic_attack(self, target):
        dam = (self.mana * 0.9) + (self.intellect * 0.5) + (self.damage * 0.3)
        dam_random = random.randint(1, int(dam))
        
        for artifact in self.artifacts:
            if artifact.get('type') == 'magic_boost':
                dam_random = int(dam_random * (1 + artifact['value']))
        
        target.take_damage(dam_random)
        self.mp -= 20
        return dam_random
    
    def heal_spell(self, target):
        if self.mp >= 30:
            heal_amount = (self.intellect * 0.8) + (self.mana * 0.4)
            heal_random = random.randint(1, int(heal_amount))
            target.heal(heal_random)
            self.mp -= 30
            return heal_random
        return 0

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, "Лучник", hp=120, mp=60, strength=40, agility=100, intellect=30, damage=60)

    def ranged_attack(self, target):
        dam = (self.agility * 0.8) + (self.damage * 0.7)
        dam_random = random.randint(1, int(dam))

        for artifact in self.artifacts:
            if artifact.get('type') == 'precision_boost':
                dam_random = int(dam_random * (1 + artifact['value']))

        target.take_damage(dam_random)
        self.mp -= 12

        if random.random() < 0.25:  # 25% шанс
            critical_damage = int(dam_random * 0.8)  # 80% от основного урона
            target.take_damage(critical_damage)
            print(f"✨ {self.name} совершает меткий выстрел! Дополнительный урон: {critical_damage}")
            return dam_random + critical_damage

        return dam_random

class Healer(Character):
    def __init__(self, name):
        super().__init__(name, "Целитель", hp=130, mp=150, strength=20, agility=30, intellect=80, damage=20)
        self.mana = 70
    
    def heal(self, target):
        heal_amount = (self.mana * 0.8) + (self.intellect * 0.9)
        heal_random = random.randint(1, int(heal_amount))
        target.heal(heal_random)
        self.mp -= 15
        return heal_random
    
    def restore_mana(self, target, amount):
        if self.mp >= amount:
            target.restore_mp(amount)
            self.mp -= int(amount/2)
            return amount
        return 0

class Enemy:
    """Класс врага"""
    def __init__(self, name, enemy_type, hp, mp, strength, damage, special=None):
        self.name = name
        self.enemy_type = enemy_type
        self.max_hp = hp
        self.hp = hp
        self.mp = mp
        self.strength = strength
        self.damage = damage
        self.special = special
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0


    def attack(self, target):
        dam = (self.strength * 0.7) + (self.damage * 0.5)
        dam_random = random.randint(1, int(dam))
        target.take_damage(dam_random)
        return dam_random
    
    @property
    def is_alive(self):
        return self.hp > 0
    
    def __str__(self):
        return f"{self.name} ({self.enemy_type}): HP={self.hp}/{self.max_hp}"

# Создаем различные типы врагов
class Goblin(Enemy):
    def __init__(self, name, strength_level=1):
        hp = 80 * strength_level
        damage = 25 * strength_level
        super().__init__(name, "Гоблин", hp, 30, 50 * strength_level, damage)

class Orc(Enemy):
    def __init__(self, name):
        super().__init__(name, "Орк", 200, 50, 120, 60)

class DarkMage(Enemy):
    def __init__(self, name):
        super().__init__(name, "Темный маг", 150, 200, 40, 30)

class Dragon(Enemy):
    def __init__(self, name):
        super().__init__(name, "Дракон", 500, 300, 200, 100)

class GameStory:
    """Класс для управления сюжетом"""
    def __init__(self):
        self.current_branch = None
        self.chapter = 1
        self.artifacts_found = []
        self.story_flags = {}
    
    def start_story(self):
        print("\n\n        ПРОЛОГ: ТЬМА НАД КОРОЛЕВСТВОМ АЛЬВАРИЯ\n")

        print("\nДавным-давно, в королевстве Альвария, царили мир и процветание.")
        print("Но однажды из глубины Теневых гор поднялся древний злодей - Морганар.")
        print("Он запечатал магию королевства и призвал армии тьмы.")
        print("\nТы, как один из последних защитников Альварии, должен собрать команду")
        print("и найти древние артефакты, чтобы победить зло.")
        print("\nТвоя судьба зависит от выбора, который ты сделаешь...")
        
        input("\nНажми Enter, чтобы продолжить...")
    
    def show_branch_choice(self):
        print("\nВЫБОР ПУТИ:")
        print("\nКуда ты отправишься в поисках артефактов?")
        print("1. Путь Воина - В Леса Эльфов (Сила и Защита)")
        print("2. Путь Мага - В Башню Чародеев (Магия и Мудрость)")
        print("3. Путь Искателя - В Подземелья Гномов (Сокровища и Хитрость)")
        
        while True:
            choice = input("\nВыбери путь (1-3): ")
            if choice in ['1', '2', '3']:
                self.current_branch = int(choice)
                self.chapter = 1
                return self.current_branch
            print("Пожалуйста, выбери 1, 2 или 3")
    
    def play_chapter(self, branch, chapter, team, artifacts):
        if branch == 1:
            return self._warrior_branch(chapter, team, artifacts)
        elif branch == 2:
            return self._mage_branch(chapter, team, artifacts)
        elif branch == 3:
            return self._explorer_branch(chapter, team, artifacts)
    
    def _warrior_branch(self, chapter, team, artifacts):
        if chapter == 1:
            print("\nГЛАВА 1: ЛЕСА ЭЛЬФОВ")
            
            print("\nТы направляешься в древние Леса Эльфов, где, по легендам,")
            print("хранится Меч Солнца - оружие, способное поразить любого врага.")
            print("\nПо пути ты встречаешь Эльфийского Стража...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Goblin("Гоблин-разведчик"),
                'artifact': {
                    'name': 'Эльфийский амулет',
                    'type': 'agility_boost',
                    'value': 0.2,
                    'description': 'Увеличивает ловкость на 20%'
                },
                'text': 'Эльфийский страж доверяет тебе и дарует амулет.',
                'next_chapter': 2
            }
        
        elif chapter == 2:
            print("\nГЛАВА 2: ХРАМ ДРЕВНИХ")
            
            print("\nВ глубине леса ты находишь древний храм.")
            print("Его охраняют каменные големы, созданные древними магами.")
            print("\nСможешь ли ты пройти эту защиту?")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Orc("Орк-хранитель"),
                'artifact': {
                    'name': 'Щит Древних',
                    'type': 'defense_boost',
                    'value': 0.3,
                    'description': 'Увеличивает максимальное HP на 30%'
                },
                'text': 'Ты нашел древний щит в руинах храма!',
                'next_chapter': 3
            }
        
        elif chapter == 3:
            print("\nГЛАВА 3: ДОЛИНА ИСПЫТАНИ")
            
            print("\nТы дошел до Долины Испытаний, где тебя ждет последнее")
            print("испытание перед встречей с финальным врагом.")
            print("\nЗдесь обитают могущественные существа...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Orc("Вождь гоблинов Грох'тар"),
                'artifact': {
                    'name': 'Меч Солнца',
                    'type': 'attack_boost',
                    'value': 0.4,
                    'description': 'Увеличивает атаку на 40%'
                },
                'text': 'Ты нашел легендарный Меч Солнца!',
                'next_chapter': 4
            }
    
    def _mage_branch(self, chapter, team, artifacts):
        if chapter == 1:
            print("\nГЛАВА 1: БАШНЯ ЧАРОДЕЕВ")

            print("\nТы поднимаешься по крутым ступеням Башни Чародеев,")
            print("где хранится Глаз Провидца - артефакт великой магической силы.")
            print("\nБашня полна магических ловушек и стражей...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Goblin("Гоблин-вор"),
                'artifact': {
                    'name': 'Свиток Огня',
                    'type': 'magic_boost',
                    'value': 0.25,
                    'description': 'Увеличивает магическую силу на 25%'
                },
                'text': 'Ты нашел древний магический свиток!',
                'next_chapter': 2
            }
        
        elif chapter == 2:
            print("\nГЛАВА 2: БИБЛИОТЕКА ТАЙН")
            
            print("\nВ глубине башни ты находишь древнюю библиотеку,")
            print("где хранятся знания, способные изменить мир.")
            print("\nНо знания охраняют магические стражи...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': DarkMage("Темный ученик"),
                'artifact': {
                    'name': 'Гримуар Вечности',
                    'type': 'intellect_boost',
                    'value': 0.3,
                    'description': 'Увеличивает интеллект на 30%'
                },
                'text': 'Ты нашел древний гримуар с потерянными знаниями!',
                'next_chapter': 3
            }
    
    def _explorer_branch(self, chapter, team, artifacts):
        if chapter == 1:
            print("\nГЛАВА 1: ПОДЗЕМЕЛЬЯ ГНОМОВ")
            
            print("\nТы спускаешься в темные подземелья, где гномы")
            print("хранят Камень Душ - артефакт невероятной силы.")
            print("\nТемнота скрывает множество опасностей...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Goblin("Пещерный гоблин", strength_level=2),
                'artifact': {
                    'name': 'Карта Сокровищ',
                    'type': 'luck_boost',
                    'value': 0.15,
                    'description': 'Увеличивает шанс критического удара'
                },
                'text': 'Ты нашел старую карту сокровищ!',
                'next_chapter': 2
            }
        
        elif chapter == 2:
            print("\nГЛАВА 2: ЗАЛ СОКРОВИЩ")
            
            print("\nСледуя по карте, ты находишь Зал Сокровищ,")
            print("где хранятся несметные богатства древних цивилизаций.")
            print("\nНо сокровища охраняют механические стражи...")
            input("\nНажми Enter, чтобы продолжить...")
            
            return {
                'enemy': Orc("Орк-наемник"),
                'artifact': {
                    'name': 'Камень Душ',
                    'type': 'hp_boost',
                    'value': 0.35,
                    'description': 'Увеличивает максимальное здоровье на 35%'
                },
                'text': 'Ты нашел легендарный Камень Душ!',
                'next_chapter': 3
            }
    
    def get_final_battle(self, branch):
        if branch == 1:
            return Dragon("Дракон Теней")
        elif branch == 2:
            return DarkMage("Морганар")
        elif branch == 3:
            return Orc("Вождь орков Гром'гар")

def create_team():
    """Создание команды персонажей"""
    print("\nСОЗДАНИЕ КОМАНДЫ:")
    
    team = []
    available_classes = {
        '1': ('Воин', Warrior),
        '2': ('Маг', Mage),
        '3': ('Лучник', Archer),
        '4': ('Целитель', Healer)
    }
    
    print("\nСоздай свою команду (4-6 персонажей):")
    print("1. Воин - Сильный защитник, отличный урон в ближнем бою")
    print("2. Маг - Мощные заклинания, слабая защита")
    print("3. Лучник - Точные дальние атаки, высокая ловкость")
    print("4. Целитель - Исцеление союзников, поддержка")
    
    team_size = 0
    while team_size < 4 or team_size > 6:
        try:
            team_size = int(input("\nСколько персонажей в команде? (4-6): "))
            if team_size < 4 or team_size > 6:
                print("Команда должна быть от 4 до 6 персонажей!")
        except ValueError:
            print("Пожалуйста, введи число!")
    
    for i in range(team_size):
        print(f"\n--- Персонаж {i+1} ---")
        print("Выбери класс:")
        for key, (name, _) in available_classes.items():
            print(f"{key}. {name}")
        
        while True:
            choice = input("Твой выбор (1-4): ")
            if choice in available_classes:
                char_name = input("Имя персонажа: ")
                char_class = available_classes[choice][1]
                character = char_class(char_name)
                team.append(character)
                print(f"Добавлен {available_classes[choice][0]} - {char_name}")
                break
            else:
                print("Пожалуйста, выбери от 1 до 4")
    
    return team

def battle(team, enemy, artifacts=[]):
    """Проведение битвы"""
    print(f"\n⚔️  БИТВА С {enemy.name.upper()} ⚔️")
    print(f"Тип: {enemy.enemy_type}")
    print(f"Здоровье: {enemy.hp}")
    print("-"*30)
    
    round_num = 1
    
    while enemy.is_alive and any(char.is_alive for char in team):
        print(f"\n--- Раунд {round_num} ---")
        
        # Ход команды
        for i, char in enumerate(team):
            if char.is_alive and enemy.is_alive:
                print(f"\nХод {char.name} ({char.char_type})")
                print(f"HP: {char.hp}/{char.max_hp}, MP: {char.mp}/{char.max_mp}")
                
                if isinstance(char, Warrior):
                    damage = char.war_attack(enemy)
                    print(f"{char.name} атакует! Урон: {damage}")
                elif isinstance(char, Mage):
                    # Маг может атаковать или лечить
                    print("1 - Атаковать, 2 - Лечить союзника")
                    action = input("Выбери действие: ")
                    if action == '2' and char.mp >= 30:
                        print("Кого исцелить?")
                        for j, ally in enumerate(team):
                            if ally.is_alive:
                                print(f"{j+1}. {ally.name} (HP: {ally.hp})")
                        try:
                            target_idx = int(input("Выбери цель: ")) - 1
                            if 0 <= target_idx < len(team) and team[target_idx].is_alive:
                                heal = char.heal_spell(team[target_idx])
                                print(f"{char.name} исцеляет {team[target_idx].name} на {heal} HP")
                        except:
                            damage = char.magic_attack(enemy)
                            print(f"{char.name} атакует магией! Урон: {damage}")
                    else:
                        damage = char.magic_attack(enemy)
                        print(f"{char.name} атакует магией! Урон: {damage}")
                elif isinstance(char, Archer):
                    damage = char.ranged_attack(enemy)
                    print(f"{char.name} стреляет! Урон: {damage}")
                elif isinstance(char, Healer):
                    # Целитель может лечить или восстанавливать ману
                    print("1 - Лечить, 2 - Восстановить ману")
                    action = input("Выбери действие: ")
                    if action == '1':
                        print("Кого исцелить?")
                        for j, ally in enumerate(team):
                            if ally.is_alive:
                                print(f"{j+1}. {ally.name} (HP: {ally.hp})")
                        try:
                            target_idx = int(input("Выбери цель: ")) - 1
                            if 0 <= target_idx < len(team) and team[target_idx].is_alive:
                                heal = char.heal(team[target_idx])
                                print(f"{char.name} исцеляет {team[target_idx].name} на {heal} HP")
                        except:
                            heal = char.heal(char)
                            print(f"{char.name} исцеляет себя на {heal} HP")
                    else:
                        print("Кому восстановить ману?")
                        for j, ally in enumerate(team):
                            if ally.is_alive:
                                print(f"{j+1}. {ally.name} (MP: {ally.mp})")
                        try:
                            target_idx = int(input("Выбери цель: ")) - 1
                            if 0 <= target_idx < len(team) and team[target_idx].is_alive:
                                amount = int(input("Сколько маны восстановить? (10-50): "))
                                restored = char.restore_mana(team[target_idx], amount)
                                if restored > 0:
                                    print(f"{char.name} восстанавливает {restored} MP {team[target_idx].name}")
                        except:
                            heal = char.heal(char)
                            print(f"{char.name} исцеляет себя на {heal} HP")
        
        # Проверка, жив ли враг
        if not enemy.is_alive:
            print(f"\n🎉 {enemy.name} побежден! 🎉")
            return True
        
        # Ход врага
        if enemy.is_alive:
            # Враг атакует случайного живого персонажа
            alive_chars = [char for char in team if char.is_alive]
            if alive_chars:
                target = random.choice(alive_chars)
                damage = enemy.attack(target)
                print(f"\n{enemy.name} атакует {target.name}! Урон: {damage}")
                print(f"{target.name}: HP = {target.hp}")
                
                if not target.is_alive:
                    print(f"💀 {target.name} пал в бою! 💀")
        
        round_num += 1
    
    # Проверка результата битвы
    if enemy.is_alive:
        print(f"\n💀 Ваша команда потерпела поражение от {enemy.name} 💀")
        return False
    else:
        return True

def main():
    """Основная функция игры"""
    print("\nБИТВА ЗА АЛЬВАРИЮ\n")
    
    # Инициализируем систему сохранений
    game_state = GameState()
    
    # Показываем меню
    while True:
        print("\nГЛАВНОЕ МЕНЮ:\n")
        print("1. Новая игра")
        print("2. Загрузить сохранение")
        print("3. Посмотреть статистику")
        print("4. Выход")
        
        choice = input("\nВыбери действие (1-4): ")
        
        if choice == '1':
            start_new_game(game_state)
        elif choice == '2':
            load_game(game_state)
        elif choice == '3':
            game_state.show_statistics()
        elif choice == '4':
            print("Спасибо за игру! До свидания!")
            break
        else:
            print("Неверный выбор. Попробуй снова.")

def start_new_game(game_state):
    """Запуск новой игры"""
    print("\nНОВАЯ ИГРА")
    
    player_name = input("\nВведи имя своего героя: ")
    
    # Создаем команду
    team = create_team()
    
    # Инициализируем сюжет
    story = GameStory()
    story.start_story()
    
    # Выбираем ветку сюжета
    branch = story.show_branch_choice()
    
    # Проходим главы
    artifacts = []
    current_chapter = 1
    game_completed = False
    
    while current_chapter <= 3 and not game_completed:
        chapter_data = story.play_chapter(branch, current_chapter, team, artifacts)
        
        if not chapter_data:
            print("Ошибка загрузки главы!")
            break
        
        print(f"\n{chapter_data['text']}")
        
        # Битва
        victory = battle(team, chapter_data['enemy'], artifacts)
        
        if victory:
            print("\n🎉 ПОБЕДА! 🎉")
            
            # Получаем артефакт
            artifact = chapter_data['artifact']
            artifacts.append(artifact)
            print(f"\nВы получили артефакт: {artifact['name']}")
            print(f"Описание: {artifact['description']}")
            
            # Применяем артефакт к случайному персонажу
            if team:
                alive_chars = [char for char in team if char.is_alive]
                if alive_chars:
                    target_char = random.choice(alive_chars)
                    target_char.add_artifact(artifact)
                    print(f"{artifact['name']} теперь принадлежит {target_char.name}")
            
            # Сохраняем игру
            game_state.save_game(
                player_name=player_name,
                team=team,
                artifacts=artifacts,
                story_branch=branch,
                chapter=current_chapter,
                outcome='victory'
            )
            
            current_chapter = chapter_data.get('next_chapter', current_chapter + 1)
            
            if current_chapter > 3:
                # Финальная битва
                final_boss = story.get_final_battle(branch)
                print("\nФИНАЛЬНАЯ БИТВА")
                print(f"\nТы дошел до финального противника - {final_boss.name}!")
                print("От этой битвы зависит судьба всего королевства!")
                input("\nНажми Enter, чтобы начать финальную битву...")
                
                final_victory = battle(team, final_boss, artifacts)
                
                if final_victory:
                    print("\nПОБЕДА!")
                    print(f"\nТы победил {final_boss.name} и спас королевство Альвария!")
                    print("Твое имя будет вписано в летописи королевства навеки!")
                    print(f"\nНайденные артефакты: {len(artifacts)}")
                    for art in artifacts:
                        print(f"- {art['name']}: {art['description']}")
                    
                    game_state.save_game(
                        player_name=player_name,
                        team=team,
                        artifacts=artifacts,
                        story_branch=branch,
                        chapter='final',
                        outcome='complete_victory'
                    )
                else:
                    print(f"\nТы пал в битве с {final_boss.name}...")
                    print("Королевство погрузилось во тьму на тысячу лет...")
                    
                    game_state.save_game(
                        player_name=player_name,
                        team=team,
                        artifacts=artifacts,
                        story_branch=branch,
                        chapter='final',
                        outcome='defeat'
                    )
                
                game_completed = True
                break
            
            # Продолжение
            continue_choice = input("\nПродолжить путешествие? (да/нет): ").lower()
            if continue_choice != 'да':
                print("Игра сохранена. Возвращайся в любое время!")
                break
        else:
            print("\nИгра окончена. Попробуй снова!")
            
            game_state.save_game(
                player_name=player_name,
                team=team,
                artifacts=artifacts,
                story_branch=branch,
                chapter=current_chapter,
                outcome='defeat'
            )
            break
    
    if game_completed:
        input("\nНажми Enter, чтобы вернуться в главное меню...")

def load_game(game_state):
    """Загрузка сохраненной игры"""
    saves = game_state.load_saves_list()
    
    if not saves:
        print("\nНет сохраненных игр")
        return
    
    game_state.show_saves()
    
    try:
        save_choice = int(input("\nВыбери номер сохранения для просмотра (0 для отмены): "))
        if save_choice == 0:
            return
        
        if 1 <= save_choice <= len(saves):
            save_info = game_state.load_save(save_choice - 1)
            
            if save_info:
                load_choice = input("\nНачать новую игру с этими параметрами? (да/нет): ").lower()
                if load_choice == 'да':
                    print("\nЗагрузка игры...")
                    print("Функция полной загрузки в разработке...")
                    print("Пока что можно только посмотреть информацию о сохранении")
    except ValueError:
        print("Неверный ввод")

if __name__ == "__main__":
    main()