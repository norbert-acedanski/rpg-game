import random

class Spell:
    def __init__(self, name, cost, damage, tajp):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.tajp = tajp

    def generateDamage(self):
        magicDamageLow = self.damage - 15
        magicDamageHigh = self.damage + 15
        return random.randrange(magicDamageLow, magicDamageHigh)