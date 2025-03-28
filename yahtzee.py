import random

class Dice:
    def __init__(self, num_dice=5):
        self.num_dice = num_dice
        self.values = [random.randint(1, 6) for _ in range(num_dice)]  # Initialize with random values
        self.held = [False] * num_dice  # Track held dice

    def roll(self, hold=None):
        if hold is None:
            hold = [False] * self.num_dice
        self.held = hold
        for i in range(self.num_dice):
            if not self.held[i]:
                self.values[i] = random.randint(1, 6)
        return self.values

    def hold_die(self, die_index):
        self.held[die_index] = True

    def release_die(self, die_index):
        self.held[die_index] = False

class Turn:
    def __init__(self):
        self.rolls = 0
        self.dice = Dice()

    def roll_dice(self, hold=None):
        if self.rolls < 3:
            self.dice.roll(hold)
            self.rolls += 1
            print(f"Rolled dice: {self.dice.values}")
            return self.dice.values
        else:
            return None  # No more rolls allowed

    def hold_die(self, die_index):
        self.dice.hold_die(die_index)

    def release_die(self, die_index):
        self.dice.release_die(die_index)

    def reset_turn(self):
        self.rolls = 0
        self.dice = Dice()

class GameState:
    def __init__(self):
        self.scores = {
            "Ones": None,
            "Twos": None,
            "Threes": None,
            "Fours": None,
            "Fives": None,
            "Sixes": None,
            "Three of a Kind": None,
            "Four of a Kind": None,
            "Full House": None,
            "Small Straight": None,
            "Large Straight": None,
            "Yahtzee": None,
            "Chance": None,
        }
        self.turn = Turn()
        self.game_over = False  # Track if the game is over
        self.current_roll = []  # Store dice values from the current roll
        self.held_dice = []  # Store indices of held dice
        
    def update_score(self, category, score):
        if category in self.scores and self.scores[category] is None:
            self.scores[category] = score
            return True  # Score updated successfully
        return False  # Score update failed (category used or invalid)

    def calculate_upper_section_bonus(self):
        upper_section_score = 0
        for category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
            if self.scores[category] is not None:
                upper_section_score += self.scores[category]
        if upper_section_score >= 63:
            return 35
        else:
            return 0
    
    def calculate_grand_total(self):
        grand_total = 0
        for score in self.scores.values():
            if score is not None:
                grand_total += score
        grand_total += calculate_upper_section_bonus()        
        return grand_total
        
    def is_game_over(self):
        return all(value is not None for value in self.scores.values())
    
class YahtzeeScorer:
    @staticmethod
    def calculate_score(roll, category):
        if category == "Ones":
            return sum(value for value in roll if value == 1)
        if category == "Twos":
            return sum(value for value in roll if value == 2)
        if category == "Threes":
            return sum(value for value in roll if value == 3)
        if category == "Fours":
            return sum(value for value in roll if value == 4)
        if category == "Fives":
            return sum(value for value in roll if value == 5)
        if category == "Sixes":
            return sum(value for value in roll if value == 6)
        if category == "Three of a Kind":
            counts = {}
            for value in roll:
                counts[value] = counts.get(value, 0) + 1
            for count in counts.values():
                if count >= 3:
                    return sum(roll)
            return 0
        if category == "Four of a Kind":
            counts = {}
            for value in roll:
                counts[value] = counts.get(value, 0) + 1
            for count in counts.values():
                if count >= 4:
                    return sum(roll)
            return 0
        if category == "Full House":
            counts = {}
            for value in roll:
                counts[value] = counts.get(value, 0) + 1
            if counts and len(counts) == 2 and (3 in counts.values() and 2 in counts.values()):
                return 25
            return 0
        if category == "Small Straight":
            roll_set = set(roll)
            small_straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
            for straight in small_straights:
                if straight.issubset(roll_set):
                    return 30
            return 0
        if category == "Large Straight":
            roll_set = set(roll)
            small_straights = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
            for straight in small_straights:
                if straight.issubset(roll_set):
                    return 40
            return 0
        if category == "Chance":
            return sum(roll)
        if category == "Yahtzee":
            counts = {}
            for value in roll:
                counts[value] = counts.get(value, 0) + 1
            for count in counts.values():
                if count == 5:
                    return 50
            return 0
        # ... other scoring categories will go here

# Example usage
dice = Dice()
roll = dice.roll()
print(f"Rolled dice: {roll}")

score = YahtzeeScorer.calculate_score(roll, "Yahtzee") # Example category
print(f"Score for Yahtzee: {score}")