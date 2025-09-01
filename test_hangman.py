import unittest
import time
from hangman import HangmanGame, LIVES, TIMER_LIMIT

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        # Initialize a basic game with known word
        self.game = HangmanGame(level='basic')
        self.game.level = 'basic'
        self.game.answer = 'apple'
        self.game.display = ['_' for _ in self.game.answer]
        self.game.lives = LIVES
        self.game.guessed = set()
        self.game.start_time = time.time()
        self.game.timer = TIMER_LIMIT
        self.game.game_over = False
        self.game.win = False

    def test_initial_display(self):
        self.assertEqual(self.game.get_display_word(), '_ _ _ _ _')

    def test_correct_guess(self):
        self.game.answer = 'apple'
        self.game.display = ['_' for _ in self.game.answer]
        self.game.guess('a')
        # Only the first 'a' in 'apple' should be revealed
        self.assertEqual(self.game.display, ['a', '_', '_', '_', '_'])

    def test_incorrect_guess_deducts_life(self):
        self.game.guess('z')
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_win_condition(self):
        # Guess all unique letters in 'apple'
        for letter in set(self.game.answer):
            self.game.guess(letter)
        self.assertTrue(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_lose_condition(self):
        # Use unique wrong guesses to reduce lives to 0
        wrong_letters = ['z', 'x', 'q', 'v', 'm', 'n']
        for letter in wrong_letters:
            self.game.guess(letter)
        self.assertFalse(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_timer_deducts_life(self):
        # Simulate timer running out
        self.game.start_time -= (TIMER_LIMIT + 1)
        self.game.update_timer()
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_random_word_selection(self):
        self.game.level = 'basic'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["python", "hangman", "school", "programming", "testing"])

    def test_random_phrase_selection(self):
        self.game.level = 'intermediate'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["open source", "unit test", "software engineering", "artificial intelligence"])

    def test_phrase_guess(self):
        self.game.level = 'intermediate'
        self.game.answer = 'hello world'
        self.game.display = ['_' if c.isalpha() else c for c in self.game.answer]
        self.game.guess('o')
        self.assertEqual(self.game.display, ['_', '_', '_', '_', 'o', ' ', '_', 'o', '_', '_', '_'])

if __name__ == '__main__':
    unittest.main()
