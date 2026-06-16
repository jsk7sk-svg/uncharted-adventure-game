import random
import json
import os

SAVE_FILE = "uncharted_save.json"


class Uncharted:

    # ─────────────────────────── UTILITIES ───────────────────────────

    @staticmethod
    def exit_game():
        print("\nThanks for playing! See you next time.")
        exit()

    @staticmethod
    def get_gamer_name():
        name = input("Please enter your name (or type 'quit' to exit): ").strip()
        if name.lower() == "quit":
            Uncharted.exit_game()
        return name

    @staticmethod
    def display_status(player_health, enemy_health, max_player=100, max_enemy=None):
        """Render a side-by-side health bar display."""

        def bar(hp, max_hp, width=20):
            filled = max(0, int((hp / max_hp) * width))
            return "[" + "█" * filled + "░" * (width - filled) + f"] {max(0, hp)}/{max_hp}"

        max_enemy = max_enemy or enemy_health
        print("\n" + "─" * 50)
        print(f"  YOU  {bar(player_health, max_player)}")
        print(f"ENEMY  {bar(enemy_health, max_enemy)}")
        print("─" * 50)

    # ─────────────────────────── SAVE / LOAD ─────────────────────────

    @staticmethod
    def save_game(state: dict):
        with open(SAVE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"  [Game saved to {SAVE_FILE}]")

    @staticmethod
    def load_game() -> dict | None:
        if not os.path.exists(SAVE_FILE):
            return None
        with open(SAVE_FILE) as f:
            return json.load(f)

    @staticmethod
    def save_prompt(state: dict):
        ans = input("\nSave progress? (y/n): ").strip().lower()
        if ans == "y":
            Uncharted.save_game(state)

    # ─────────────────────────── SETUP ───────────────────────────────

    @staticmethod
    def choose_difficulty():
        difficulties = {
            "easy": {"enemy_health": 80, "enemy_attack": (5, 20), "enemies": 1},
            "normal": {"enemy_health": 100, "enemy_attack": (10, 30), "enemies": 2},
            "hard": {"enemy_health": 120, "enemy_attack": (15, 40), "enemies": 3},
            "crushing": {"enemy_health": 150, "enemy_attack": (20, 50), "enemies": 3},
        }
        while True:
            choice = input(
                "\nSelect difficulty (Easy, Normal, Hard, Crushing) or type 'quit' to exit: "
            ).strip().lower()
            if choice == "quit":
                Uncharted.exit_game()
            if choice in difficulties:
                return choice, difficulties[choice]
            print("Invalid choice. Please select a valid difficulty level.")

    @staticmethod
    def choose_character():
        characters = {
            "Nathan Drake": {"desc": "Increased shooting accuracy", "bonus": "accuracy"},
            "Sully Sullivan": {"desc": "Higher chance to dodge attacks", "bonus": "dodge"},
            "Elena Fisher": {"desc": "Finds extra health packs", "bonus": "healer"},
            "Samuel Drake": {"desc": "Deals more melee damage", "bonus": "melee"},
            "Chloe Frazer": {"desc": "Starts with an extra weapon", "bonus": "extra_weapon"},
        }
        while True:
            print("\nSelect your character:")
            for char, info in characters.items():
                print(f"  • {char} — {info['desc']}")
            choice = input("Which character do you choose? (or type 'quit' to exit): ").title()
            if choice.lower() == "quit":
                Uncharted.exit_game()
            if choice in characters:
                return choice, characters[choice]
            print("Invalid character choice. Try again.")

    @staticmethod
    def choose_game():
        games = {
            "1": "Uncharted: Drake's Fortune",
            "2": "Uncharted: Among Thieves",
            "3": "Uncharted: Drake's Deception",
            "4": "Uncharted: A Thief's End",
        }
        while True:
            print("\nChoose an Uncharted World to Spawn into:")
            for key, value in games.items():
                print(f"  {key}: {value}")
            choice = input("Enter the number (1-4) or type 'quit' to exit: ").strip()
            if choice.lower() == "quit":
                Uncharted.exit_game()
            if choice in games:
                return games[choice]
            print("Invalid choice. Try again.")

    # ─────────────────────────── EXPLORATION ─────────────────────────

    @staticmethod
    def adventure_choice(inventory, character_info):
        print("\nYou are in a dense jungle, following ruins of an ancient civilisation.")
        print("Suddenly you hear a rustling in the bushes.\n")

        choices = {
            "1": "Investigate the noise.",
            "2": "Keep moving cautiously.",
            "3": "Take cover and prepare your weapon.",
        }
        for key, value in choices.items():
            print(f"  {key}: {value}")

        while True:
            choice = input("What do you do? (1/2/3) or 'quit': ").strip()
            if choice.lower() == "quit":
                Uncharted.exit_game()

            if choice == "1":
                print("\nYou discover a hidden pathway. You find a health pack and a grenade!")
                inventory["Health Pack"] += 1
                inventory["Grenade"] += 1
                break
            elif choice == "2":
                print("\nYou move cautiously and avoid unnecessary danger.")
                # Elena: passive ability fires here
                if character_info["bonus"] == "healer":
                    inventory["Health Pack"] += 1
                    print("Elena's keen eye spots a half-buried med kit — you grab it!")
                break
            elif choice == "3":
                print("\nYou take cover, ready for a fight… it was just a monkey!")
                break
            else:
                print("Invalid choice. Try again.")

    # ─────────────────────────── COMBAT ──────────────────────────────

    @staticmethod
    def combat(difficulty_settings, inventory, character, character_info, enemy_num=1):
        enemy_max_hp = difficulty_settings["enemy_health"]
        enemy_health = enemy_max_hp
        player_health = 100
        player_max_hp = 100

        ammo = {
            "Primary": 5,
            "Extra": 3 if character_info["bonus"] == "extra_weapon" else 0,
        }

        dodge_chance = 30 if character_info["bonus"] == "dodge" else 15

        loot_pool = ["Health Pack", "Grenade", "Gold Idol Shard", "Ancient Coin"]

        print(f"\n{'=' * 50}")
        print(f"  ⚔  ENEMY ENCOUNTER {enemy_num}  ⚔")
        print(f"{'=' * 50}")
        print("An enemy mercenary spots you! Prepare for battle.\n")

        while enemy_health > 0 and player_health > 0:
            Uncharted.display_status(player_health, enemy_health, player_max_hp, enemy_max_hp)

            print("\nActions:")
            print(f"  1: Shoot          (Ammo: {ammo['Primary']})")
            if character_info["bonus"] == "extra_weapon":
                print(f"  2: Extra Weapon   (Ammo: {ammo['Extra']})")
            print(f"  3: Melee Attack")
            print(f"  4: Dodge")
            print(f"  5: Health Pack    (x{inventory['Health Pack']})")
            print(f"  6: Grenade        (x{inventory['Grenade']})")
            print(f"  q: Quit Game")

            action = input("\nYour move: ").strip().lower()

            if action == "q":
                Uncharted.exit_game()

            acted = True
            if action == "1":
                if ammo["Primary"] <= 0:
                    print("  Out of primary ammo!")
                    acted = False
                else:
                    base = (25, 50) if character_info["bonus"] == "accuracy" else (20, 40)
                    damage = random.randint(*base)
                    enemy_health -= damage
                    ammo["Primary"] -= 1
                    print(f"  You shoot → {damage} damage! Enemy HP: {max(0, enemy_health)}")

            elif action == "2":
                if character_info["bonus"] != "extra_weapon":
                    print("  You don't have an extra weapon.")
                    acted = False
                elif ammo["Extra"] <= 0:
                    print("  Extra weapon is out of ammo!")
                    acted = False
                else:
                    damage = random.randint(35, 60)
                    enemy_health -= damage
                    ammo["Extra"] -= 1
                    print(f"  Extra weapon fires → {damage} damage! Enemy HP: {max(0, enemy_health)}")

            elif action == "3":
                # Samuel Drake deals bonus melee damage
                base = (20, 45) if character_info["bonus"] == "melee" else (10, 25)
                damage = random.randint(*base)
                enemy_health -= damage
                bonus_tag = " [MELEE BONUS]" if character_info["bonus"] == "melee" else ""
                print(f"  Melee strike{bonus_tag} → {damage} damage! Enemy HP: {max(0, enemy_health)}")

            elif action == "4":
                if random.randint(1, 100) <= dodge_chance:
                    print("  You dodge the attack!")
                    continue  # skip enemy turn entirely
                else:
                    print("  Dodge failed — you still take a hit!")
                    # enemy attacks below

            elif action == "5":
                if inventory["Health Pack"] <= 0:
                    print("  No health packs left!")
                    acted = False
                else:
                    inventory["Health Pack"] -= 1
                    heal = 30
                    player_health = min(player_max_hp, player_health + heal)
                    print(f"  You use a health pack → HP restored to {player_health}")
                    # Using a health pack doesn't end the enemy's turn
                    enemy_attack = random.randint(*difficulty_settings["enemy_attack"])
                    player_health -= enemy_attack
                    print(f"  Enemy attacks for {enemy_attack}! Your HP: {max(0, player_health)}")
                    if player_health <= 0:
                        print("\n  You've been defeated. Game over.")
                        Uncharted.exit_game()
                    continue

            elif action == "6":
                if inventory["Grenade"] <= 0:
                    print("  No grenades left!")
                    acted = False
                else:
                    damage = random.randint(40, 70)
                    enemy_health -= damage
                    inventory["Grenade"] -= 1
                    print(f"  BOOM! Grenade → {damage} damage! Enemy HP: {max(0, enemy_health)}")

            else:
                print("  Unknown action.")
                acted = False

            # Enemy counter-attack (if the player took an offensive/failed action)
            if acted and enemy_health > 0:
                enemy_attack = random.randint(*difficulty_settings["enemy_attack"])
                player_health -= enemy_attack
                print(f"  Enemy hits back for {enemy_attack}! Your HP: {max(0, player_health)}")
                if player_health <= 0:
                    print("\n  You've been defeated. Game over.")
                    Uncharted.exit_game()

        # ── Victory ──
        print(f"\n  ★ Enemy defeated!")
        drop = random.choice(loot_pool)
        inventory[drop] = inventory.get(drop, 0) + 1
        print(f"  You loot the body and find: {drop}!")
        if enemy_num == 1:
            inventory["Ancient Key"] = inventory.get("Ancient Key", 0) + 1
            print("  You also find an Ancient Key on the ground...")

    # ─────────────────────────── PUZZLE ──────────────────────────────

    @staticmethod
    def temple_puzzle(inventory):
        print("\n" + "=" * 50)
        print("  🏛  THE STONE DOOR PUZZLE")
        print("=" * 50)
        print(
            "\nBefore you stands a massive stone door carved with glyphs.\n"
            "Three symbols must be aligned to open it.\n"
            "Each symbol is a riddle — answer correctly.\n"
        )

        riddles = [
            {
                "q": "I speak without a mouth and hear without ears.\n"
                     "I have no body, but I come alive with wind. What am I?",
                "a": "echo",
                "hint": "(think about what bounces back in a cave…)",
            },
            {
                "q": "The more you take, the more you leave behind. What am I?",
                "a": "footsteps",
                "hint": "(think about what you make when you walk…)",
            },
            {
                "q": "I have cities, but no houses live there.\n"
                     "I have mountains, but no trees grow there.\n"
                     "I have water, but no fish swim there. What am I?",
                "a": "map",
                "hint": "(an explorer's best friend…)",
            },
        ]

        solved = 0
        for i, riddle in enumerate(riddles, 1):
            print(f"\n  — Symbol {i} of 3 —")
            print(f"  {riddle['q']}")
            attempts = 2

            while attempts > 0:
                answer = input("  Your answer: ").strip().lower()
                if answer == "quit":
                    Uncharted.exit_game()
                if answer == riddle["a"]:
                    print("  ✔ Correct! The symbol glows.")
                    solved += 1
                    break
                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"  ✘ Wrong. One attempt left. Hint: {riddle['hint']}")
                    else:
                        print("  ✘ The symbol stays dark.")

        print(f"\n  You solved {solved}/3 symbols.")
        if solved == 3:
            print(
                "\n  The door rumbles and swings open!\n"
                "  Inside: golden light, ancient treasure — and a map to the next ruin.\n"
                "  Your legend grows, adventurer."
            )
            inventory["Treasure Map"] = 1
            inventory["Gold Idol"] = 1
        elif solved >= 2:
            print(
                "\n  The door creaks open just enough to squeeze through.\n"
                "  You grab what you can before it slams shut."
            )
            inventory["Ancient Coin"] = inventory.get("Ancient Coin", 0) + 2
        else:
            print(
                "\n  The door does not open. A trap triggers — you barely escape.\n"
                "  The treasure remains hidden… for now."
            )

    # ─────────────────────────── ENDING ──────────────────────────────

    @staticmethod
    def ending(gamer_name, inventory, difficulty_name, character):
        print("\n" + "=" * 50)
        print("  📜  CHAPTER ONE COMPLETE")
        print("=" * 50)
        print(f"\n  Well done, {gamer_name}!")
        print(f"  Character : {character}")
        print(f"  Difficulty: {difficulty_name.title()}")
        print("\n  — Final Inventory —")
        for item, count in inventory.items():
            if count:
                print(f"    {item}: {count}")
        print(
            "\n  To be continued in Chapter Two:\n"
            "  'The Forgotten Temple' awaits beyond the jungle…\n"
        )


# ──────────────────────────── MAIN ────────────────────────────────────


def main():
    global inventory, character_info, difficulty, character, gamer_name, difficulty_name
    print("\n" + "=" * 50)
    print("    U N C H A R T E D  —  Fan Adventure")
    print("=" * 50)

    # Offer to load a previous save
    save = Uncharted.load_game()
    if save:
        resume = input("\nA saved game was found. Resume? (y/n): ").strip().lower()
        if resume == "y":
            state = save
            gamer_name = state["gamer_name"]
            difficulty_name = state["difficulty_name"]
            difficulty = state["difficulty"]
            character = state["character"]
            character_info = state["character_info"]
            game = state["game"]
            inventory = state["inventory"]
            stage = state["stage"]
            print(f"\nWelcome back, {gamer_name}! Resuming at stage: {stage}")
        else:
            stage = None
    else:
        stage = None

    if not stage:
        inventory = {
            "Health Pack": 0,
            "Grenade": 0,
            "Ancient Key": 0,
        }
        gamer_name = Uncharted.get_gamer_name()
        print(f"\nHello {gamer_name}! Welcome to the Uncharted adventure. Be careful what you wish for…\n")

        difficulty_name, difficulty = Uncharted.choose_difficulty()
        character, character_info = Uncharted.choose_character()
        print(f"\nGreat choice! {character} — ability: {character_info['desc']}\n")

        game = Uncharted.choose_game()
        print(f"\nWelcome to {game}! Let the adventure begin…\n")
        stage = "exploration"

    # Helper to build save state
    def make_state(current_stage):
        return {
            "gamer_name": gamer_name,
            "difficulty_name": difficulty_name,
            "difficulty": difficulty,
            "character": character,
            "character_info": character_info,
            "game": game,
            "inventory": inventory,
            "stage": current_stage,
        }

    # ── Stage: Exploration ──
    if stage == "exploration":
        Uncharted.adventure_choice(inventory, character_info)
        stage = "combat_1"
        Uncharted.save_prompt(make_state(stage))

    # ── Stage: Combat encounters ──
    num_enemies = difficulty["enemies"]
    for enemy_num in range(1, num_enemies + 1):
        stage_key = f"combat_{enemy_num}"
        if stage == stage_key:
            print(f"\n— Encounter {enemy_num} of {num_enemies} —")
            Uncharted.combat(difficulty, inventory, character, character_info, enemy_num)
            next_stage = f"combat_{enemy_num + 1}" if enemy_num < num_enemies else "puzzle"
            stage = next_stage
            Uncharted.save_prompt(make_state(stage))

    # ── Stage: Puzzle ──
    if stage == "puzzle":
        input("\n(Press Enter to approach the stone door…)")
        Uncharted.temple_puzzle(inventory)
        stage = "ending"
        Uncharted.save_prompt(make_state(stage))

    # ── Ending ──
    Uncharted.ending(gamer_name, inventory, difficulty_name, character)


if __name__ == "__main__":
    main()
