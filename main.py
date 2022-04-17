import random

from game import Person, bcolors
from magic import Spell
from inventory import Item

fire = Spell("Fire", 25, 600, "Black Magic")
thunder = Spell("Thunder", 25, 600, "Black Magic")
blizzard = Spell("Blizzard", 25, 600, "Black Magic")
meteor = Spell("Meteor", 50, 1200, "Black Magic")
quake = Spell("Quake", 35, 740, "Black Magic")

cure = Spell("Cure", 25, 620, "White Magic")
cura = Spell("Cura", 35, 1500, "White Magic")
curaga = Spell("Curaga", 50, 6000, "White Magic")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
HI_potion = Item("HI-Potion", "potion", "Heals 100 HP", 100)
super_potion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
HI_elixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_magic = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": HI_potion, "quantity": 5}, 
                {"item": super_potion, "quantity": 5}, {"item": elixer, "quantity": 5}, 
                {"item": HI_elixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

player_1 = Person("Predator", 3260, 132, 300, 34, player_magic, player_items)
player_2 = Person("Tommy", 4160, 188, 311, 34, player_magic, player_items)
player_3 = Person("Claude", 3089, 174, 288, 34, player_magic, player_items)
enemy_1 = Person("Tars ", 5250, 130, 560, 325, enemy_magic, [])
enemy_2 = Person("Magus", 18200, 701, 525, 25, enemy_magic, [])
enemy_3 = Person("Goran", 5250, 130, 560, 325, enemy_magic, [])

players = [player_1, player_2, player_3]
enemies = [enemy_1, enemy_2, enemy_3]

running = True

def format_names():
    max_player_name_length = 0
    for player in players:
        if len(player.name) > max_player_name_length:
            max_player_name_length = len(player.name)
    for player in players:
        player.name += " "*(max_player_name_length - len(player.name))
    max_enemy_name_length = 0
    for enemy in enemies:
        if len(enemy.name) > max_enemy_name_length:
            max_enemy_name_length = len(enemy.name)
    for enemy in enemies:
        enemy.name += " "*(max_enemy_name_length - len(enemy.name))

if __name__ == "__main__":
    format_names()
    print(bcolors.FAIL + bcolors.BOLD + "Enemy attacks!" + bcolors.ENDC)
    while running:
        print("======================================================================================================================================================================")
        print("NAME                   HP                                     MP")
        for player in players:
            player.get_stats()
        for enemy in enemies:
            enemy.get_enemy_stats()
        for player in players:
            player.choose_action()
            choice = input("Choose action: ")
            action_index = int(choice) - 1
            if action_index == -1:
                running = False
                continue
            elif action_index == 0:
                player_damage = player.generate_damage()
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(player_damage)
                print(bcolors.OKGREEN + "You attacked " + enemies[enemy].name.replace(" ", "") + " for", player_damage, "points of damage." + bcolors.ENDC)
                if enemies[enemy].HP == 0:
                    print(enemies[enemy].name.replace(" ", "") + " died!")
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
                    print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(player_damage), "HP." + bcolors.ENDC)
                elif spell.typ == "Black Magic":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(player_damage)
                    print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(player_damage), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                    if enemies[enemy].HP == 0:
                        print(enemies[enemy].name.replace(" ", "") + " died!")
                        del enemies[enemy]
            elif action_index == 2:
                player.choose_item()
                item_choice = int(input("Choose item: ")) - 1
                if item_choice == -1:
                    continue
                item = player.items[item_choice]["item"]
                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                    continue
                player.items[item_choice]["quantity"] -= 1
                if item.typ == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
                elif item.typ == "elixer":
                    if item.name == "Mega Elixer":
                        for player in players:
                            player.HP = player.max_HP
                            player.magic_points = player.max_magic_points
                    else:
                        player.HP = player.max_HP
                        player.magic_points = player.max_magic_points
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP and MP" + bcolors.ENDC)
                elif item.typ == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                    if enemies[enemy].HP == 0:
                        print(enemies[enemy].name.replace(" ", "") + " died!")
                        del enemies[enemy]
        defeated_enemies = 0
        defeated_players = 0
        for enemy in enemies:
            if enemy.HP == 0:
                defeated_enemies += 1
        for player in players:
            if player.HP == 0:
                defeated_players += 1
        if defeated_enemies == len(enemies):
            print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
            running = False
        elif defeated_players == len(players):
            print(bcolors.FAIL + "Your enemies defeated you!" + bcolors.ENDC)
            running = False
        print("\n")
        for enemy in enemies:
            enemy_choice = random.randrange(0, 2)
            if enemy_choice == 0:
                target = random.randrange(0, len(players))
                enemy_damage = enemies[0].generate_damage()
                players[target].take_damage(enemy_damage)
                print(bcolors.FAIL + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" " ":", "") + " for", enemy_damage, "points of damage." + bcolors.ENDC)
            elif enemy_choice == 1:
                spell, magic_damage = enemy.choose_enemy_spell()
                enemy.reduce_magic_points(spell.cost)
                if spell.typ == "White Magic":
                    enemy.heal(magic_damage)
                    print(bcolors.OKBLUE + "\n" + spell.name + " heals" + enemy.name + " for " + str(magic_damage), "HP." + bcolors.ENDC)
                elif spell.typ == "Black Magic":
                    target = random.randrange(0, len(players))
                    players[target].take_damage(magic_damage)
                    print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_damage), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
                    if players[target].HP == 0:
                        print(players[target].name.replace(" ", "") + " died!")
                        del players[target]
                print("Enemy chose", spell.name.replace(" ", ""), "with", magic_damage, "damage.")