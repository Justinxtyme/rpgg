class Magic:
    def __init__(self, name, magic_type,):
        self.name = name

class Divination(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect
class Sorcery(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect

class Pyromancy(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect

class BloodMagic(Magic):
    def __init__(self, name, magic_type, mp_cost, effect):
        super().__init__(name, magic_type)
        self.mp_cost = mp_cost
        self.effect = effect
