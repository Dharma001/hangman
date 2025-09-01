
import unittest
import time
from hangman import HangmanGame, LIVES, TIMER_LIMIT


class TestAssignmentRequirements(unittest.TestCase):
    def setUp(self):
        self.words = ["apple", "banana"]
        self.phrases = ["hello world", "open ai"]
        self.game = HangmanGame(level='basic')
        self.game.level = 'basic'
        self.game.answer = "apple"
        self.game.display = ['_' for _ in self.game.answer]
        self.game.lives = LIVES
        self.game.guessed = set()
        self.game.start_time = time.time()
        self.game.timer = TIMER_LIMIT
        self.game.game_over = False
        self.game.win = False

    def test_random_word_selection(self):
        self.game.level = 'basic'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["python", "hangman", "school", "programming", "testing"])

    def test_random_phrase_selection(self):
        self.game.level = 'intermediate'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["open source", "unit test", "software engineering", "artificial intelligence"])

    def test_underscores_for_missing_letters(self):
        self.game.answer = "apple"
        self.game.display = ['_' for _ in self.game.answer]
        self.assertEqual(self.game.get_display_word(), '_ _ _ _ _')

    def test_timer_deducts_life(self):
        self.game.start_time -= (TIMER_LIMIT + 1)
        self.game.update_timer()
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_correct_guess_reveals_all(self):
        self.game.answer = "banana"
        self.game.display = ['_' for _ in self.game.answer]
        self.game.guess('a')
        self.assertEqual(self.game.display, ['_', 'a', '_', 'a', '_', 'a'])

    def test_incorrect_guess_deducts_life(self):
        self.game.guess('z')
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_win_condition(self):
        for letter in set(self.game.answer):
            self.game.guess(letter)
        self.assertTrue(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_lose_condition(self):
        for _ in range(LIVES):
            self.game.guess('z')
        self.assertFalse(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_game_continues_until_quit_or_lost(self):
        self.assertFalse(self.game.game_over)
        self.game.guess('z')
        self.assertFalse(self.game.game_over)
        for _ in range(LIVES-1):
            self.game.guess('z')
        self.assertTrue(self.game.game_over)

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
        self.game.guess('a')
        # All 'a's should be revealed
        self.assertEqual(self.game.display, ['a', '_', '_', '_', 'e']) if self.game.answer == 'apple' else self.assertIn('a', self.game.display)

    def test_incorrect_guess(self):
        self.game.guess('z')
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_win_condition(self):
        for letter in set(self.game.answer):
            self.game.guess(letter)
        self.assertTrue(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_lose_condition(self):
        for _ in range(LIVES):
            self.game.guess('z')
        self.assertFalse(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_timer_deducts_life(self):
        # Simulate timeout
        self.game.start_time -= (TIMER_LIMIT + 1)
        self.game.update_timer()
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_phrase_level(self):
        # Test intermediate/phrase level
        self.game.level = 'intermediate'
        self.game.answer = 'hello world'
        self.game.display = ['_' if c.isalpha() else c for c in self.game.answer]
        self.game.guess('o')
        self.assertEqual(self.game.display, ['_', '_', '_', '_', 'o', ' ', '_', 'o', '_', '_', '_'])

if __name__ == '__main__':
    unittest.main()
