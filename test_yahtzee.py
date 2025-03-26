import unittest
from yahtzee import Dice, Turn, YahtzeeScorer

class TestDice(unittest.TestCase):
    def test_roll(self):
        dice = Dice()
        roll = dice.roll()
        self.assertEqual(len(roll), 5)  # Check if 5 dice are rolled
        for value in roll:
            self.assertTrue(1 <= value <= 6)  # Check if dice values are within range


class TestTurn(unittest.TestCase):
    def test_initial_state(self):
        turn = Turn()
        self.assertIsInstance(turn.dice, Dice)
        self.assertEqual(turn.rolls, 0)
    def test_roll_dice(self):
        turn = Turn()
        self.assertEqual(turn.rolls, 0)  
        turn1 = turn.roll_dice()
        self.assertEqual(turn.rolls, 1)   
        turn2 = turn.roll_dice()
        self.assertEqual(turn.rolls, 2)                     
        turn3 = turn.roll_dice()
        self.assertEqual(turn.rolls, 3)
        turn4 = turn.roll_dice()
        self.assertIsNone(turn4)
        self.assertEqual(turn.rolls, 3)  

    def test_hold_release_dice(self):
        turn = Turn()
        turn.roll_dice()  # Ensure dice are rolled first

        turn.hold_die(0)
        self.assertTrue(turn.dice.held[0])

        turn.release_die(0)
        self.assertFalse(turn.dice.held[0])

    def test_reset_turn(self):
        turn = Turn()
        turn.roll_dice()
        turn.hold_die(0)
        oldDice = turn.dice
        turn.reset_turn()
        newDice = turn.dice

        self.assertEqual(turn.rolls, 0)
        self.assertIsInstance(newDice, Dice)
        self.assertIsNot(oldDice, newDice)
        self.assertFalse(turn.dice.held[0])

class TestYahtzeeScorer(unittest.TestCase):
    def test_calculate_score_ones(self):
        roll = [1, 1, 2, 3, 4]
        score = YahtzeeScorer.calculate_score(roll, "Ones")
        self.assertEqual(score, 2)

        roll = [1, 1, 1, 1, 1]
        score = YahtzeeScorer.calculate_score(roll, "Ones")
        self.assertEqual(score, 5)

        roll = [2, 3, 4, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Ones")
        self.assertEqual(score, 0)

    def test_calculate_score_twos(self):
        roll = [1, 1, 2, 3, 4]
        score = YahtzeeScorer.calculate_score(roll, "Twos")
        self.assertEqual(score, 2)

        roll = [1, 2, 2, 2, 5]
        score = YahtzeeScorer.calculate_score(roll, "Twos")
        self.assertEqual(score, 6)

        roll = [1, 3, 4, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Twos")
        self.assertEqual(score, 0)

    def test_calculate_score_threes(self):
        roll = [1, 1, 2, 3, 4]
        score = YahtzeeScorer.calculate_score(roll, "Threes")
        self.assertEqual(score, 3)

        roll = [1, 2, 3, 3, 5]
        score = YahtzeeScorer.calculate_score(roll, "Threes")
        self.assertEqual(score, 6)

        roll = [1, 2, 4, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Threes")
        self.assertEqual(score, 0)

    def test_calculate_score_fours(self):
        roll = [1, 1, 2, 3, 4]
        score = YahtzeeScorer.calculate_score(roll, "Fours")
        self.assertEqual(score, 4)

        roll = [1, 2, 4, 4, 4]
        score = YahtzeeScorer.calculate_score(roll, "Fours")
        self.assertEqual(score, 12)

        roll = [1, 2, 3, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Fours")
        self.assertEqual(score, 0)

    def test_calculate_score_fives(self):
        roll = [1, 1, 2, 3, 5]
        score = YahtzeeScorer.calculate_score(roll, "Fives")
        self.assertEqual(score, 5)

        roll = [5, 5, 3, 3, 5]
        score = YahtzeeScorer.calculate_score(roll, "Fives")
        self.assertEqual(score, 15)

        roll = [1, 2, 4, 3, 6]
        score = YahtzeeScorer.calculate_score(roll, "Fives")
        self.assertEqual(score, 0)
        
    def test_calculate_score_sixes(self):
        roll = [6, 1, 2, 3, 4]
        score = YahtzeeScorer.calculate_score(roll, "Sixes")
        self.assertEqual(score, 6)

        roll = [1, 6, 3, 6, 5]
        score = YahtzeeScorer.calculate_score(roll, "Sixes")
        self.assertEqual(score, 12)

        roll = [1, 2, 4, 5, 3]
        score = YahtzeeScorer.calculate_score(roll, "Sixes")
        self.assertEqual(score, 0)

    def test_calculate_score_three_of_a_kind(self):
        roll = [3, 3, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Three of a Kind")
        self.assertEqual(score, 18)

        roll = [2, 2, 2, 2, 5]
        score = YahtzeeScorer.calculate_score(roll, "Three of a Kind")
        self.assertEqual(score, 13)

        roll = [1, 2, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Three of a Kind")
        self.assertEqual(score, 0)

    def test_calculate_score_four_of_a_kind(self):
        roll = [3, 3, 3, 3, 5]
        score = YahtzeeScorer.calculate_score(roll, "Four of a Kind")
        self.assertEqual(score, 17)

        roll = [2, 2, 2, 2, 2]
        score = YahtzeeScorer.calculate_score(roll, "Four of a Kind")
        self.assertEqual(score, 10)

        roll = [1, 2, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Four of a Kind")
        self.assertEqual(score, 0)

    def test_calculate_score_full_house(self):
        roll = [3, 3, 3, 5, 5]
        score = YahtzeeScorer.calculate_score(roll, "Full House")
        self.assertEqual(score, 25)

        roll = [2, 2, 5, 5, 5]
        score = YahtzeeScorer.calculate_score(roll, "Full House")
        self.assertEqual(score, 25)

        roll = [2, 5, 2, 5, 5]
        score = YahtzeeScorer.calculate_score(roll, "Full House")
        self.assertEqual(score, 25)

        roll = [1, 2, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Full House")
        self.assertEqual(score, 0)

        roll = [2,2,2,2,5]
        score = YahtzeeScorer.calculate_score(roll, "Full House")
        self.assertEqual(score, 0)

    def test_calculate_score_small_straight(self):
        roll = [1, 2, 3, 4, 6]
        score = YahtzeeScorer.calculate_score(roll, "Small Straight")
        self.assertEqual(score, 30)

        roll = [2, 3, 4, 5, 1]
        score = YahtzeeScorer.calculate_score(roll, "Small Straight")
        self.assertEqual(score, 30)

        roll = [3, 4, 5, 6, 2]
        score = YahtzeeScorer.calculate_score(roll, "Small Straight")
        self.assertEqual(score, 30)

        roll = [2, 5, 4, 2, 3]
        score = YahtzeeScorer.calculate_score(roll, "Small Straight")
        self.assertEqual(score, 30)

        roll = [1, 2, 3, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Small Straight")
        self.assertEqual(score, 0)
    
    def test_calculate_large_small_straight(self):
        roll = [1, 2, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Large Straight")
        self.assertEqual(score, 40)

        roll = [2, 3, 4, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Large Straight")
        self.assertEqual(score, 40)

        roll = [3, 4, 5, 6, 2]
        score = YahtzeeScorer.calculate_score(roll, "Large Straight")
        self.assertEqual(score, 40)

        roll = [2, 5, 4, 2, 3]
        score = YahtzeeScorer.calculate_score(roll, "Large Straight")
        self.assertEqual(score, 0)

        roll = [1, 2, 3, 5, 6]
        score = YahtzeeScorer.calculate_score(roll, "Large Straight")
        self.assertEqual(score, 0)

    def test_calculate_score_chance(self):
        roll = [1, 2, 3, 4, 5]
        score = YahtzeeScorer.calculate_score(roll, "Chance")
        self.assertEqual(score, 15)

        roll = [6, 6, 6, 6, 6]
        score = YahtzeeScorer.calculate_score(roll, "Chance")
        self.assertEqual(score, 30)

        roll = [1, 1, 1, 1, 6]
        score = YahtzeeScorer.calculate_score(roll, "Chance")
        self.assertEqual(score, 10)
    
    def test_calculate_score_yahtzee(self):
        roll = [3, 3, 3, 3, 3]
        score = YahtzeeScorer.calculate_score(roll, "Yahtzee")
        self.assertEqual(score, 50)

        roll = [1, 1, 1, 1, 1]
        score = YahtzeeScorer.calculate_score(roll, "Yahtzee")
        self.assertEqual(score, 50)

        roll = [3, 3, 3, 3, 5]
        score = YahtzeeScorer.calculate_score(roll, "Yahtzee")
        self.assertEqual(score, 0)

if __name__ == "__main__":
    unittest.main()