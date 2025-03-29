class Magic:
    def __init__(self, name, magic_type, mp_cost, effect):
        self.name = name
        self.magic_type = magic_type
        self.mp_cost = mp_cost
        self.effect = effect
        self.scaling = scaling
    
    def cast(self, caster, target):
        base_damage = self.effect(caster, target)
        scaling_damage = 0
        for attribute, factor in self.scaling.items():
            attribute_value = getattr(caster, attribute, 0)
            scaling_damage += attribute_value * factor
        total_damage = (base_damage + scaling_damage)
        return total_damage
        
class Divination(Magic):
    def __init__(self, name, magic_type, mp_cost, effect, scaling):
        super().__init__(name, magic_type, mp_cost, effect, scaling)
      
class Sorcery(Magic):
    def __init__(self, name, magic_type, mp_cost, effect, scaling):
        super().__init__(name, magic_type, mp_cost, effect, scaling)

class Pyromancy(Magic):
    def __init__(self, name, magic_type, mp_cost, effect, scaling):
        super().__init__(name, magic_type, mp_cost, effect, scaling)

class BloodMagic(Magic):
    def __init__(self, name, magic_type, mp_cost, effect, scaling):
        super().__init__(name, magic_type, mp_cost, effect, scaling)
      
class BladeMagic(Magic):
    def __init__(self, name, magic_type, mp_cost, effect, scaling):
        super().__init__(name, magic_type, mp_cost, effect, scaling)

minor_blessing = Divination(name="Minor Blessing", magic_type="Divination", mp_cost=20, effect=normal_heal)
fire_blast = Pyromancy(name="Fire Blast", magic_type="Pyromancy", mp_cost=20, effect=fire_burst)
blood_call = BloodMagix(name="Blood Call", magic_type ="Blood Magic",mp_cost=20, effect=None)


spell_objects = {

}