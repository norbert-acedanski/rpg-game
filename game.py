import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:

    def __init__(self, name, HP, magicPoints, attack, defence, magic, items):
        self.maxHP = HP
        self.name = name
        self.HP = HP
        self.maxMagicPoints = magicPoints
        self.magicPoints = magicPoints
        self.attackLow = attack - 10
        self.attackHigh = attack + 10
        self.defence = defence
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generateDamage(self):
        return random.randrange(self.attackLow, self.attackHigh)

    def takeDamage(self, damage):
        self.HP -= damage
        if self.HP < 0:
            self.HP = 0
        return self.HP

    def heal(self, damage):
        self.HP +=damage
        if self.HP > self.maxHP:
            self.HP = self.maxHP
        
    def getHP(self):
        return self.HP
    
    def getMaxHP(self):
        return self.maxHP
    
    def getMagicPoints(self):
        return self.magicPoints

    def getMaxMagicPoints(self):
        return self.maxMagicPoints

    def reduceMagicPoints(self, cost):
        self.magicPoints -=cost

    def chooseAction(self):
        i = 1
        print("\n    " + bcolors.BOLD + bcolors.UNDERLINE + self.name + bcolors.ENDC)
        print(bcolors.OKGREEN + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i +=1

    def chooseMagic(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(cost: ", str(spell.cost) + ")")
            i +=1

    def chooseItem(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["item"].name +  ": ", str(item["item"].description) + "(x" + str(item["quantity"]) + ")")
            i +=1

    def chooseTarget(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.getHP() != 0:
                print("    " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("Choose target: ")) - 1
        return choice


    def getEnemyStats(self):
        HPBar = ""
        barThicks = self.HP/self.maxHP*50
        while barThicks > 0:
            HPBar += "█"
            barThicks -= 1
        while len(HPBar) < 50:
            HPBar += " "
        print("                     __________________________________________________")
        print(bcolors.BOLD + self.name + "   " + 
              "%5d/%5d" % (self.HP, self.maxHP) + " |" + bcolors.FAIL + HPBar + bcolors.ENDC + bcolors.BOLD + "|")

    def getStats(self):
        HPBar = ""
        MPBar = ""
        HPBarTicks = self.HP/self.maxHP*25
        MPBarThicks = self.magicPoints/self.maxMagicPoints*10
        while HPBarTicks > 0:
            HPBar += "█"
            HPBarTicks -= 1
        while len(HPBar) < 25:
            HPBar += " "
        while MPBarThicks > 0:
            MPBar += "█"
            MPBarThicks -= 1
        while len(MPBar) < 10:
            MPBar += " "
        print("                       _________________________              __________")
        print(bcolors.BOLD + self.name + "   " + 
              "%4d/%4d" % (self.HP, self.maxHP) + " |" + bcolors.OKGREEN + HPBar + bcolors.ENDC + bcolors.BOLD + "|    " + 
              "%3d/%3d" % (self.magicPoints, self.maxMagicPoints) + " |" + bcolors.OKBLUE + MPBar + bcolors.ENDC + "|")
    
    def chooseEnemySpell(self):
        magicChoice = random.randrange(0, len(self.magic))
        spell = self.magic[magicChoice]
        magicDamage = spell.generateDamage()
        if self.magicPoints < spell.cost or spell.tajp == "white" and self.HP/self.maxHP*100 > 50:
            self.chooseEnemySpell()
        else:
            return spell, magicDamage