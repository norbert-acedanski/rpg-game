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

    def __init__(self, name, HP, magic_points, attack, defence, magic, items):
        self.max_HP = HP
        self.name = name
        self.HP = HP
        self.max_magic_points = magic_points
        self.magic_points = magic_points
        self.attack_low = attack - 10
        self.attack_high = attack + 10
        self.defence = defence
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_high)

    def take_damage(self, damage):
        self.HP -= damage
        if self.HP < 0:
            self.HP = 0
        return self.HP

    def heal(self, damage):
        self.HP +=damage
        if self.HP > self.max_HP:
            self.HP = self.max_HP
        
    def get_HP(self):
        return self.HP
    
    def get_max_HP(self):
        return self.max_HP
    
    def get_magic_points(self):
        return self.magic_points

    def get_max_magic_points(self):
        return self.max_magic_points

    def reduce_magic_points(self, cost):
        self.magic_points -=cost

    def choose_action(self):
        i = 1
        print("\n    " + bcolors.BOLD + bcolors.UNDERLINE + self.name + bcolors.ENDC)
        print(bcolors.OKGREEN + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i +=1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(cost: ", str(spell.cost) + ")")
            i +=1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["item"].name +  ": ", str(item["item"].description) + "(x" + str(item["quantity"]) + ")")
            i +=1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_HP() != 0:
                print("    " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("Choose target: ")) - 1
        return choice


    def get_enemy_stats(self):
        HP_bar = ""
        bar_thicks = self.HP/self.max_HP*50
        while bar_thicks > 0:
            HP_bar += "█"
            bar_thicks -= 1
        while len(HP_bar) < 50:
            HP_bar += " "
        print("                     __________________________________________________")
        print(bcolors.BOLD + self.name + "   " + 
              "%5d/%5d" % (self.HP, self.max_HP) + " |" + bcolors.FAIL + HP_bar + bcolors.ENDC + bcolors.BOLD + "|")

    def get_stats(self):
        HP_bar = ""
        MP_bar = ""
        HP_bar_ticks = self.HP/self.max_HP*25
        MP_bar_thicks = self.magic_points/self.max_magic_points*10
        while HP_bar_ticks > 0:
            HP_bar += "█"
            HP_bar_ticks -= 1
        while len(HP_bar) < 25:
            HP_bar += " "
        while MP_bar_thicks > 0:
            MP_bar += "█"
            MP_bar_thicks -= 1
        while len(MP_bar) < 10:
            MP_bar += " "
        print("                       _________________________              __________")
        print(bcolors.BOLD + self.name + "   " + 
              "%4d/%4d" % (self.HP, self.max_HP) + " |" + bcolors.OKGREEN + HP_bar + bcolors.ENDC + bcolors.BOLD + "|    " + 
              "%3d/%3d" % (self.magic_points, self.max_magic_points) + " |" + bcolors.OKBLUE + MP_bar + bcolors.ENDC + "|")
    
    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_damage = spell.generate_damage()
        if self.magic_points < spell.cost or spell.typ == "white" and self.HP/self.max_HP*100 > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_damage