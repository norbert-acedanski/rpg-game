import random

from game import Person, bcolors
from magic import Spell
from inventory import Item

fire     = Spell("Fire", 25, 600, "Black Magic")
thunder  = Spell("Thunder", 25, 600, "Black Magic")
blizzard = Spell("Blizzard", 25, 600, "Black Magic")
meteor   = Spell("Meteor", 50, 1200, "Black Magic")
quake    = Spell("Quake", 35, 740, "Black Magic")

cure   = Spell("Cure", 25, 620, "White Magic")
cura   = Spell("Cura", 35, 1500, "White Magic")
curaga = Spell("Curaga", 50, 6000, "White Magic")

potion       = Item("Potion", "potion", "Heals 500 HP", 500)
HI_potion    = Item("HI-Potion", "potion", "Heals 1000 HP", 1000)
super_potion = Item("Super Potion", "potion", "Heals 5000 HP", 5000)
MP_potion    = Item("MP-Potion", "mp-potion", "Restores 50 MP", 50)
elixer       = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
HI_elixer    = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_magic  = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": HI_potion, "quantity": 5}, 
                {"item": super_potion, "quantity": 5}, {"item": MP_potion, "quantity": 10},
                {"item": elixer, "quantity": 5}, {"item": HI_elixer, "quantity": 2}, 
                {"item": grenade, "quantity": 5}]

player_1 = Person("Predator", 3260, 132, 300, 34, player_magic, player_items)
player_2 = Person("Tommy", 4160, 188, 311, 34, player_magic, player_items)
player_3 = Person("Claude", 3089, 174, 288, 34, player_magic, player_items)

enemy_1 = Person("Tars ", 5250, 130, 560, 325, enemy_magic, [])
enemy_2 = Person("Magus", 18200, 701, 525, 25, enemy_magic, [])
enemy_3 = Person("Goran", 5250, 130, 560, 325, enemy_magic, [])

players = [player_1, player_2, player_3]
enemies = [enemy_1, enemy_2, enemy_3]

number_of_players = len(players)
number_of_enemies = len(enemies)

running = True


def format_names():
    max_player_name_length = 0
    max_enemy_name_length = 0
    for player in players:
        if len(player.name) > max_player_name_length:
            max_player_name_length = len(player.name)
    for player in players:
        player.name += " "*(max_player_name_length - len(player.name))
    for enemy in enemies:
        if len(enemy.name) > max_enemy_name_length:
            max_enemy_name_length = len(enemy.name)
    for enemy in enemies:
        enemy.name += " "*(max_enemy_name_length - len(enemy.name))


def show_stats():
    print("="*166)
    print("NAME".ljust(23) + "HP".ljust(37) + "MP")
    for player in players:
        player.get_player_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()


def choose_action(player):
    player.choose_action()
    return int(input("Choose action: ")) - 1


def check_endgame_condition():
    global running
    defeated_enemies = number_of_enemies - len(enemies)
    defeated_players = number_of_players - len(players)
    if defeated_enemies == number_of_enemies:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        for player in players:
            player.get_player_stats()
        running = False
    elif defeated_players == number_of_players:
        print(bcolors.FAIL + "Your enemies defeated you!" + bcolors.ENDC)
        running = False


def enemy_attack_procedure(enemy):
    if len(players) > 0:
        target = random.randrange(0, len(players))
        enemy_damage = enemies[0].generate_damage()
        players[target].take_damage(enemy_damage)
        print(bcolors.FAIL + f'{enemy.name.replace(" ", "")} attacks {players[target].name.replace(" ", "")} for '
                             f'{enemy_damage} points of damage.' + bcolors.ENDC)
        if players[target].HP == 0:
            print(f'{players[target].name.replace(" ", "")} died!')
            del players[target]


def enemy_magic_procedure(enemy):
    if enemy.HP > 0:
        spell, magic_damage = enemy.choose_enemy_spell()
        enemy.reduce_magic_points(spell.cost)
        if spell.typ == "White Magic":
            enemy.heal(magic_damage)
            print(bcolors.OKBLUE + f"\n{spell.name} heals {enemy.name} for {magic_damage} HP." + bcolors.ENDC)
        elif spell.typ == "Black Magic":
            target = random.randrange(0, len(players))
            players[target].take_damage(magic_damage)
            print(bcolors.OKBLUE + f"{enemy.name.replace(' ', '')}'s {spell.name} deals {magic_damage} "
                                   f"points of damage to {players[target].name.replace(' ', '')}" + bcolors.ENDC)
            if players[target].HP == 0:
                print(f"{players[target].name.replace(' ', '')} died!")
                del players[target]


if __name__ == "__main__":
    format_names()
    print(bcolors.FAIL + bcolors.BOLD + "Enemy attacks!" + bcolors.ENDC)
    while running:
        show_stats()
        for player in players:
            action_index = choose_action(player)
            if action_index == -1:
                running = False
                continue
            elif action_index == 0:
                if len(enemies) > 0:
                    player_damage = player.generate_damage()
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(player_damage)
                    print(bcolors.OKGREEN + f"You attacked {enemies[enemy].name.replace(' ', '')} for {player_damage} "
                                            f"points of damage." + bcolors.ENDC)
                    if enemies[enemy].HP == 0:
                        print(f"{enemies[enemy].name.replace(' ', '')} died!")
                        del enemies[enemy]
            elif action_index == 1:
                player.choose_magic()
                magic_choice = int(input("Choose magic: ")) - 1
                if magic_choice == -1:
                    continue
                spell = player.magic[magic_choice]
                player_damage = spell.generate_damage()
                current_magic_points = player.magic_points
                if spell.cost > current_magic_points:
                    print(bcolors.FAIL + "\nNot enough Magic Points\n" + bcolors.ENDC)
                    continue
                player.reduce_magic_points(spell.cost)
                if spell.typ == "White Magic":
                    player.heal(player_damage)
                    print(bcolors.OKBLUE + f"\n{spell.name} heals for {player_damage} HP." + bcolors.ENDC)
                elif spell.typ == "Black Magic":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(player_damage)
                    print(bcolors.OKBLUE + "\n" + f"\n{spell.name} deals {player_damage} points of damage to "
                                                  f"{enemies[enemy].name.replace(' ', '')}" + bcolors.ENDC)
                    if enemies[enemy].HP == 0:
                        print(f"{enemies[enemy].name.replace(' ', '')} died!")
                        del enemies[enemy]
            elif action_index == 2:
                player.choose_item()
                item_choice = int(input("Choose item: ")) - 1
                if item_choice == -1:
                    continue
                item = player.items[item_choice]["item"]
                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
                    continue
                player.items[item_choice]["quantity"] -= 1
                if item.typ == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + f"\n{item.name} heals for {item.prop} HP." + bcolors.ENDC)
                elif item.typ == "mp-potion":
                    player.reduce_magic_points(-item.prop)
                    print(bcolors.OKGREEN + f"\n{item.name} increases MP by {item.prop}" + bcolors.ENDC)
                elif item.typ == "elixer":
                    if item.name == "Mega Elixer":
                        for player in players:
                            player.HP = player.max_HP
                            player.magic_points = player.max_magic_points
                    else:
                        for player_number, player in enumerate(players, 1):
                            print(str(player_number) + ". " + bcolors.BOLD + player.name + bcolors.ENDC)
                        player_choice = int(input("Choose player to use an item on: ")) -1
                        players[player_choice].HP = players[player_choice].max_HP
                        players[player_choice].magic_points = players[player_choice].max_magic_points
                    print(bcolors.OKGREEN + f"\n{item.name} fully restores HP and MP" + bcolors.ENDC)
                elif item.typ == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + f"\n{item.name} deals {item.prop} points of damage to "
                                         f"{enemies[enemy].name.replace(' ', '')}" + bcolors.ENDC)
                    if enemies[enemy].HP == 0:
                        print(f"{enemies[enemy].name.replace(' ', '')} died!")
                        del enemies[enemy]
        if not running:
            continue
        check_endgame_condition()
        for enemy in enemies:
            enemy_choice = random.randrange(0, 2)
            if enemy_choice == 0:
                enemy_attack_procedure(enemy)
            elif enemy_choice == 1:
                enemy_magic_procedure(enemy)