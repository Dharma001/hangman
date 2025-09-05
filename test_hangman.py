import unittest
import time
from hangman import HangmanGame, LIVES, TIMER_LIMIT

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        # Initialize a basic game with a known word
        self.game = HangmanGame(level='basic')
        self.game.answer = 'apple'
        self.game.display = ['_' for _ in self.game.answer]
        self.game.lives = LIVES
        self.game.guessed = set()
        self.game.start_time = time.time()
        self.game.timer = TIMER_LIMIT
        self.game.game_over = False
        self.game.win = False

    # -------------------------
    # Basic Tests
    # -------------------------
    def test_initial_display(self):
        """Test that the initial display shows all underscores for a new word."""
        self.assertEqual(self.game.get_display_word(), '_ _ _ _ _')

    def test_correct_guess_basic(self):
        """Test that guessing a correct letter reveals all its positions in a basic word."""
        self.game.guess('p')
        self.assertEqual(self.game.display, ['_', 'p', 'p', '_', '_'])

    def test_incorrect_guess_deducts_life(self):
        """Test that an incorrect guess deducts one life."""
        self.game.guess('z')
        self.assertEqual(self.game.lives, LIVES - 1)

    def test_win_condition_basic(self):
        """Test that guessing all letters results in a win for a basic word."""
        for letter in set(self.game.answer):
            self.game.guess(letter)
        self.assertTrue(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_lose_condition_basic(self):
        """Test that too many incorrect guesses results in a loss for a basic word."""
        wrong_letters = ['z', 'x', 'q', 'v', 'm', 'n']
        for letter in wrong_letters:
            self.game.guess(letter)
        self.assertFalse(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_timer_deducts_life(self):
        """Test that the timer running out deducts a life."""
        self.game.start_time -= (TIMER_LIMIT + 1)
        self.game.update_timer()
        self.assertEqual(self.game.lives, LIVES - 1)

    # -------------------------
    # Random Selection Tests
    # -------------------------
    def test_random_word_selection(self):
        """Test that a random word is selected for the basic level."""
        self.game.level = 'basic'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["python", "hangman", "school", "programming", "testing"])

    def test_random_phrase_selection(self):
        """Test that a random phrase is selected for the intermediate level."""
        self.game.level = 'intermediate'
        self.game.pick_word()
        self.assertIn(self.game.answer, ["open source", "unit test", "software engineering", "artificial intelligence"])

    def test_random_hard_phrase_selection(self):
        """Test that a random hard phrase is selected for the hard level."""
        self.game.level = 'hard'
        self.game.pick_word()
        self.assertIn(self.game.answer, [
            "cryptography", "synchronization", "pneumonoultramicroscopicsilicovolcanoconiosis",
            "object oriented programming", "asynchronous event loop", "dijkstra's algorithm",
            "recursion depth exceeded", "differential equations", "quantum entanglement"
        ])

    # -------------------------
    # Intermediate Level Tests
    # -------------------------
    def test_phrase_guess(self):
        """Test that guessing a letter in a phrase reveals all its positions."""
        self.game.level = 'intermediate'
        self.game.answer = 'hello world'
        self.game.display = ['_' if c.isalpha() else c for c in self.game.answer]
        self.game.guess('o')
        self.assertEqual(self.game.display, ['_', '_', '_', '_', 'o', ' ', '_', 'o', '_', '_', '_'])

    # -------------------------
    # Hard Level Tests
    # -------------------------
    def test_hard_guess(self):
        """Test that guessing a letter in a hard phrase reveals all its positions."""
        self.game.level = 'hard'
        self.game.answer = 'cryptography'
        self.game.display = ['_' for _ in self.game.answer]
        self.game.guess('r')
        self.assertEqual(self.game.display, ['_', 'r', '_', '_', '_', '_', '_', 'r', '_', '_', '_', '_'])

    def test_win_condition_hard(self):
        """Test that guessing all letters results in a win for a hard phrase."""
        self.game.level = 'hard'
        self.game.answer = 'cryptography'
        self.game.display = ['_' for _ in self.game.answer]
        for letter in set(self.game.answer):
            self.game.guess(letter)
        self.assertTrue(self.game.win)
        self.assertTrue(self.game.game_over)

    def test_lose_condition_hard(self):
        """Test that too many incorrect guesses results in a loss for a hard phrase."""
        self.game.level = 'hard'
        self.game.answer = 'cryptography'
        self.game.display = ['_' for _ in self.game.answer]
        wrong_letters = ['z', 'x', 'q', 'v', 'm', 'n']
        for letter in wrong_letters:
            self.game.guess(letter)
        self.assertFalse(self.game.win)
        self.assertTrue(self.game.game_over)

if __name__ == '__main__':
    unittest.main()
