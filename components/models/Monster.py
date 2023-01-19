import time
import random

from components.models.Entity import Entity


class Monster(Entity):

    def __init__(self, data, abilities):
        super().__init__(data['hp'], data['mp'], data['stamina'], data['level'],
                         data['strength'], data['agility'], data['intellect'],
                         data['attack'], data['defense'], data['critical_hit'], data['dodge'])

        self.PROB_ABILITY = 25

        self._monster_type = data['monster_type']

        self._abilities = abilities

    @property
    def monster_type(self):
        return self._monster_type

    @property
    def abilities(self):
        return self._abilities

    # ----------------
    # Monster attacks
    # ----------------
    def monster_attack(self, character):
        if self.stat_probability(character.dodge):
            print("\nYou DODGE enemy's attack!")
        else:
            damage = self.attack - character.defense

            if damage > 0:
                if self.stat_probability(self.critical_hit):
                    damage += round(damage * 0.5)
                    print("\nCRITICAL DAMAGE!")
                    time.sleep(1)

                character.hp -= damage
            else:
                damage = 0

            print(
                f"\n{self._monster_type} deals {str(damage)} damage to {character.name}")

        time.sleep(1)

    # ------------------------
    # Monster uses an ability
    # ------------------------
    def monster_ability(self, ability, character):
        self.cast_ability(ability.resources_cost)

        if self.stat_probability(character.dodge):
            print("\nYou DODGE enemy's attack!")

        else:
            damage = ability.attack_power - character.defense

            if damage > 0:
                if self.stat_probability(self.critical_hit):
                    damage += round(damage * 0.5)
                    print("\nCRITICAL DAMAGE!")
                    time.sleep(1)

                character.hp -= damage

            print(
                f"\n{self._monster_type} use '{ability.name}' and deals {damage} damage to {character.name}")

        time.sleep(1)

    # -------------------------------
    # Gets a monster's random ability
    # -------------------------------
    def get_random_ability(self):
        prob_abilities = [ability.probability for ability in self.abilities]
        return random.choices(self.abilities, prob_abilities)[0]

    # ----------------------
    # Shows monster's stats
    # ----------------------
    def show_monster_stats(self):
        print("----------------------------------------\n"
              f"Monster: {self._monster_type}\n"
              f"Level: {self.level}\n"
              f"Floor level: {self.floor_level}\n"
              "----------------------------------------\n"
              f"data\n"
              f"----------------------------------------\n"
              f"HP = {self.hp}\n"
              f"MP = {self.mp}\n"
              f"Stamina = {self.stamina}\n"
              f"Strength = {self.strength}\n"
              f"Agility = {self.agility}\n"
              f"Intellect = {self.intellect}\n"
              f"Attack = {self.attack}\n"
              f"Defense = {self.defense}\n"
              f"Critical hit = {self.critical_hit}\n"
              f"Dodge = {self.dodge}\n"
              "----------------------------------------")

    # ------------------------------------------------------------
    # Reduces the monster's main resource when casting an ability
    # ------------------------------------------------------------
    def cast_ability(self, cost):
        if self._monster_type == "Undead":
            self.stamina -= cost
        elif self._monster_type == "Goblin":
            self.stamina -= cost
        elif self._monster_type == "Cave Spider":
            self.stamina -= cost
        elif self._monster_type == "Skeleton Warrior":
            self.stamina -= cost
        elif self._monster_type == "Dungeon Lizard":
            self.stamina -= cost
        elif self._monster_type == "Imp":
            self.mp -= cost
        elif self._monster_type == "Hellhound":
            self.stamina -= cost
        elif self._monster_type == "Shadow":
            self.mp -= cost
        elif self._monster_type == "Minotaur":
            self.stamina -= cost
        elif self._monster_type == "Stone Guardian":
            self.stamina -= cost
        elif self._monster_type == "Crystal Scorpion":
            self.stamina -= cost
        elif self._monster_type == "Wyvern":
            self.stamina -= cost
        elif self._monster_type == "Silver Fang":
            self.stamina -= cost
        elif self._monster_type == "Behemoth":
            self.mp -= cost
        elif self._monster_type == "Daemon":
            self.mp -= cost
        elif self._monster_type == "Reaper":
            self.mp -= cost
        elif self._monster_type == "Elder Lich":
            self.mp -= cost
        elif self._monster_type == "Obsidian Guardian":
            self.stamina -= cost
        elif self._monster_type == "Arachne":
            self.mp -= cost
        elif self._monster_type == "Black Dragon":
            self.mp -= cost
