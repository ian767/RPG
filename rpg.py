from dataclasses import dataclass
from typing import List
import random

@dataclass
class Environment:
    name: str
    attack_bonus: int = 0
    defense_bonus: int = 0

@dataclass
class Stronghold:
    name: str
    environment: Environment
    health: int = 100

    def apply_damage(self, damage: int):
        self.health = max(0, self.health - damage)

class Player:
    def __init__(self, race: str, player_class: str, strongholds: List[Stronghold]):
        self.race = race
        self.player_class = player_class
        self.strongholds = strongholds
        self.base_attack, self.base_defense = self.class_stats(player_class)

    @staticmethod
    def class_stats(player_class: str):
        stats = {
            "warrior": (25, 20),
            "mage": (20, 15),
            "rogue": (15, 10),
        }
        return stats.get(player_class, (20, 15))

    def is_defeated(self):
        return all(sh.health <= 0 for sh in self.strongholds)

ENVIRONMENTS = {
    "Forest": Environment("Forest", attack_bonus=0, defense_bonus=5),
    "Mountain": Environment("Mountain", attack_bonus=5, defense_bonus=0),
    "Swamp": Environment("Swamp", attack_bonus=0, defense_bonus=2),
    "Plains": Environment("Plains", attack_bonus=0, defense_bonus=0),
    "Desert": Environment("Desert", attack_bonus=2, defense_bonus=-2),
    "Volcano": Environment("Volcano", attack_bonus=10, defense_bonus=-5),
    "Ice": Environment("Ice", attack_bonus=0, defense_bonus=10),
    "River": Environment("River", attack_bonus=0, defense_bonus=5),
    "Cave": Environment("Cave", attack_bonus=2, defense_bonus=7),
    "Ruins": Environment("Ruins", attack_bonus=3, defense_bonus=0),
}

HUMAN_STRONGHOLDS = [
    ("Aurora Keep", "Plains"),
    ("Brighton Hold", "Forest"),
    ("Casterly Fort", "Mountain"),
    ("Dawn Bastion", "Forest"),
    ("Eagle Watch", "Mountain"),
    ("Falcon Reach", "Plains"),
    ("Gale Ridge", "Ruins"),
    ("Harbor Gate", "River"),
    ("Iron Guard", "Mountain"),
    ("Jade Fortress", "Forest"),
    ("Kingswatch", "Plains"),
    ("Lion's Den", "Desert"),
    ("Moonlit Spire", "Ice"),
    ("Northwatch", "Mountain"),
    ("Oakheart Hold", "Forest"),
    ("Pike's Edge", "Plains"),
    ("Queensrest", "Forest"),
    ("Riverside Citadel", "River"),
    ("Sunfire Keep", "Desert"),
    ("Tranquil Post", "Swamp"),
]

ORC_STRONGHOLDS = [
    ("Ashen Camp", "Volcano"),
    ("Bloodfang Den", "Cave"),
    ("Crimson Hold", "Swamp"),
    ("Darkmaul Outpost", "Swamp"),
    ("Ember Rock", "Volcano"),
    ("Frostbite Lair", "Ice"),
    ("Gorefield Fort", "Ruins"),
    ("Hellscream Barracks", "Volcano"),
    ("Ironmaw Stronghold", "Mountain"),
    ("Jagged Ridge", "Mountain"),
    ("Krul Camp", "Desert"),
    ("Lava Pit Base", "Volcano"),
    ("Mangrove Den", "Swamp"),
    ("Nightstalker Hideout", "Cave"),
    ("Orc Haven", "Plains"),
    ("Pitfall Hold", "Ruins"),
    ("Quake Ruins", "Ruins"),
    ("Ragefire Hold", "Volcano"),
    ("Skullcrusher Fort", "Cave"),
    ("Thornwood Camp", "Forest"),
]

def create_strongholds(data):
    return [Stronghold(name, ENVIRONMENTS[env]) for name, env in data]

def choose_option(prompt: str, options: List[str]) -> str:
    print(prompt)
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    while True:
        selection = input("Choose: ")
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            return options[int(selection) - 1]
        print("Invalid choice.")

def attack(attacker: Player, defender: Player, target: Stronghold):
    env_bonus = target.environment.defense_bonus
    damage = max(1, attacker.base_attack - env_bonus)
    target.apply_damage(damage)
    print(f"{attacker.race} {attacker.player_class} attacks {defender.race}'s {target.name} for {damage} damage. Health left: {target.health}")

def enemy_turn(enemy: Player, player: Player):
    available = [sh for sh in player.strongholds if sh.health > 0]
    if not available:
        return
    target = random.choice(available)
    attack(enemy, player, target)

def game_loop(user: Player, enemy: Player):
    round_num = 1
    while True:
        print(f"\n-- Round {round_num} --")
        if enemy.is_defeated():
            print("You have defeated all enemy strongholds!")
            break
        if user.is_defeated():
            print("All your strongholds are lost!")
            break

        # User turn
        targets = [sh for sh in enemy.strongholds if sh.health > 0]
        print("Enemy strongholds:")
        for i, sh in enumerate(targets, start=1):
            print(f"{i}. {sh.name} ({sh.health} HP, Env: {sh.environment.name})")
        choice = choose_option("Choose a stronghold to attack:", [sh.name for sh in targets])
        target = next(sh for sh in enemy.strongholds if sh.name == choice)
        attack(user, enemy, target)

        # Enemy turn
        enemy_turn(enemy, user)
        round_num += 1

def main():
    user_race = choose_option("Select your race:", ["Human", "Orc"])
    user_class = choose_option("Select your class:", ["warrior", "mage", "rogue"])

    if user_race == "Human":
        user_strongholds = create_strongholds(HUMAN_STRONGHOLDS)
        enemy_strongholds = create_strongholds(ORC_STRONGHOLDS)
        enemy_race = "Orc"
    else:
        user_strongholds = create_strongholds(ORC_STRONGHOLDS)
        enemy_strongholds = create_strongholds(HUMAN_STRONGHOLDS)
        enemy_race = "Human"

    user_player = Player(user_race, user_class, user_strongholds)
    enemy_player = Player(enemy_race, random.choice(["warrior", "mage", "rogue"]), enemy_strongholds)

    game_loop(user_player, enemy_player)

if __name__ == "__main__":
    main()
