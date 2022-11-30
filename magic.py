import random


class Spell:
    def __init__(self, name, cost, damage, typ):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.typ = typ

    def generate_damage(self):
        magic_damage_low = self.damage - 15
        magic_damage_high = self.damage + 15
        return random.randrange(magic_damage_low, magic_damage_high)
