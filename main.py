import random

from game import Person, bcolors
from magic import Spell
from inventory import Item

fire = Spell("Fire", 25, 600, "blackMagic")
thunder = Spell("Thunder", 25, 600, "blackMagic")
blizzard = Spell("Blizzard", 25, 600, "blackMagic")
meteor = Spell("Meteor", 50, 1200, "blackMagic")
quake = Spell("Quake", 35, 740, "blackMagic")

cure = Spell("Cure", 25, 620, "whiteMagic")
cura = Spell("Cura", 35, 1500, "whiteMagic")
curaga = Spell("Curaga", 50, 6000, "whiteMagic")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
HI_Potion = Item("HI-Potion", "potion", "Heals 100 HP", 100)
superPotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
HI_Elixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

playerMagic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemyMagic = [fire, meteor, curaga]
playerItems = [ {"item": potion, "quantity": 15}, {"item": HI_Potion, "quantity": 5}, 
                {"item": superPotion, "quantity": 5}, {"item": elixer, "quantity": 5}, 
                {"item": HI_Elixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Predator:", 3260, 132, 300, 34, playerMagic, playerItems)
player2 = Person("Tommy   :", 4160, 188, 311, 34, playerMagic, playerItems)
player3 = Person("Claude  :", 3089, 174, 288, 34, playerMagic, playerItems)
enemy1 = Person("Imp  ", 1250, 130, 560, 325, enemyMagic, [])
enemy2 = Person("Magus", 18200, 701, 525, 25, enemyMagic, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, enemyMagic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "Enemy attacks!" + bcolors.ENDC)

while running:
    print("================================================================================================================================================================================================================")
    print("NAME                   HP                                     MP")
    for player in players:
        player.getStats()
    for enemy in enemies:
        enemy.getEnemyStats()
    for player in players:
        player.chooseAction()
        choice = input("Choose action: ")
        actionIndex = int(choice) - 1
        if actionIndex == -1:
            running = False
            continue
        elif actionIndex == 0:
            playerDamage = player.generateDamage()
            enemy = player.chooseTarget(enemies)
            enemies[enemy].takeDamage(playerDamage)
            print(bcolors.OKGREEN + "You attacked " + enemies[enemy].name.replace(" ", "") + " for", playerDamage, "points of damage." + bcolors.ENDC)
            if enemies[enemy].getHP() == 0:
                print(enemies[enemy].name.replace(" ", "") + " died!")
                del enemies[enemy]
        elif actionIndex == 1:
            player.chooseMagic()
            magicChoice = int(input("Choose magic: ")) - 1
            if magicChoice == -1:
                continue
            spell = player.magic[magicChoice]
            playerDamage = spell.generateDamage()
            currentMagicPoints = player.getMagicPoints()
            if spell.cost > currentMagicPoints:
                print(bcolors.FAIL + "\nNot enough Magic Points\n" + bcolors.ENDC)
                continue
            player.reduceMagicPoints(spell.cost)
            if spell.tajp == "whiteMagic":
                player.heal(playerDamage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(playerDamage), "HP." + bcolors.ENDC)
            elif spell.tajp == "blackMagic":
                enemy = player.chooseTarget(enemies)
                enemies[enemy].takeDamage(playerDamage)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(playerDamage), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].getHP() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " died!")
                    del enemies[enemy]
        elif actionIndex == 2:
            player.chooseItem()
            itemChoice = int(input("Choose item: ")) - 1
            if itemChoice == -1:
                continue
            item = player.items[itemChoice]["item"]
            if player.items[itemChoice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue
            player.items[itemChoice]["quantity"] -= 1
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for player in players:
                        player.HP = player.maxHP
                        player.magicPoints = player.maxHP
                else:
                    player.HP = player.maxHP
                    player.magicPoints = player.maxHP
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP and MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.chooseTarget(enemies)
                enemies[enemy].takeDamage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].getHP() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " died!")
                    del enemies[enemy]
    defeatedEnemies = 0
    defeatedPlayers = 0
    for enemy in enemies:
        if enemy.getHP() == 0:
            defeatedEnemies += 1
    for player in players:
        if player.getHP() == 0:
            defeatedPlayers += 1
    if defeatedEnemies == len(enemies):
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeatedPlayers == len(players):
        print(bcolors.FAIL + "Your enemies defeated you!" + bcolors.ENDC)
        running = False
    print("\n")
    for enemy in enemies:
        enemyChoice = random.randrange(0, 2)
        if enemyChoice == 0:
            target = random.randrange(0, len(players))
            enemyDamage = enemies[0].generateDamage()
            players[target].takeDamage(enemyDamage)
            print(bcolors.FAIL + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" " ":", "") + " for", enemyDamage, "points of damage." + bcolors.ENDC)
        elif enemyChoice == 1:
            spell, magicDamage = enemy.chooseEnemySpell()
            enemy.reduceMagicPoints(spell.cost)
            if spell.tajp == "whiteMagic":
                enemy.heal(magicDamage)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals" + enemy.name + " for " + str(magicDamage), "HP." + bcolors.ENDC)
            elif spell.tajp == "blackMagic":
                target = random.randrange(0, len(players))
                players[target].takeDamage(magicDamage)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magicDamage), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
                if players[target].getHP() == 0:
                    print(players[target].name.replace(" ", "") + " died!")
                    del players[target]
            print("Enemy chose", spell.name.replace(" ", ""), " with", magicDamage, "damage.")