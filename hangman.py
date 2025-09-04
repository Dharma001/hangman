import random
import time
import math

# -------------------------
# Game Settings
# -------------------------
WIDTH, HEIGHT = 900, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
FONT_SIZE = 44
SMALL_FONT_SIZE = 24
LIVES = 6
TIMER_LIMIT = 15

# Word and Phrase Lists
WORDS = ["python", "hangman", "school", "programming", "testing"]
PHRASES = ["open source", "unit test", "software engineering", "artificial intelligence"]
HARD_PHRASES = [
    "cryptography", "synchronization", "pneumonoultramicroscopicsilicovolcanoconiosis",
    "object oriented programming", "asynchronous event loop", "dijkstra's algorithm",
    "recursion depth exceeded", "differential equations", "quantum entanglement"
]

# -------------------------
# Hangman Game Logic
# -------------------------
class HangmanGame:
    def __init__(self, level='basic'):
        self.level = level
        self.lives = LIVES
        self.answer = ''
        self.display = []
        self.guessed = set()
        self.start_time = time.time()
        self.timer = TIMER_LIMIT
        self.game_over = False
        self.win = False
        self.animation_progress = 0
        self.pick_word()

    def pick_word(self):
        if self.level == 'basic':
            self.answer = random.choice(WORDS)
        elif self.level == 'intermediate':
            self.answer = random.choice(PHRASES)
        elif self.level == 'hard':
            self.answer = random.choice(HARD_PHRASES)
        else:
            self.answer = random.choice(WORDS)
        self.display = ['_' if c.isalpha() else c for c in self.answer]
        self.guessed = set()
        self.lives = LIVES
        self.start_time = time.time()
        self.timer = TIMER_LIMIT
        self.game_over = False
        self.win = False
        self.animation_progress = 0

    def guess(self, letter):
        letter = letter.lower()
        if letter in self.guessed or not letter.isalpha() or self.game_over:
            return
        self.guessed.add(letter)
        if letter in self.answer:
            for i, c in enumerate(self.answer):
                if c == letter:
                    self.display[i] = letter
            if '_' not in self.display:
                self.win = True
                self.game_over = True
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True

    def update_timer(self):
        elapsed = time.time() - self.start_time
        self.timer = max(0, TIMER_LIMIT - int(elapsed))
        if self.timer == 0 and not self.game_over:
            self.lives -= 1
            self.start_time = time.time()
            self.timer = TIMER_LIMIT
            if self.lives <= 0:
                self.game_over = True

    def get_display_word(self):
        return ' '.join(self.display)

    def get_answer(self):
        return self.answer

    def animate_hanging(self):
        if self.game_over and not self.win and self.animation_progress < 30:
            self.animation_progress += 1


# -------------------------
# Pygame UI (only runs if script is executed directly)
# -------------------------
if __name__ == "__main__":
    import pygame
    import sys

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hangman Game')
    font = pygame.font.SysFont('consolas', FONT_SIZE, bold=True)
    small_font = pygame.font.SysFont('consolas', SMALL_FONT_SIZE)
    clock = pygame.time.Clock()

    # Level selection in-game
    def draw_level_menu(selected=None):
        screen.fill(WHITE)
        title = font.render('HANGMAN', True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        prompt = small_font.render('Select Level:', True, BLACK)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 160))
        levels = [
            ('1', 'Basic', 'Word'),
            ('2', 'Intermediate', 'Phrase'),
            ('3', 'Hard', 'Expert')
        ]
        for idx, (key, name, desc) in enumerate(levels):
            color = (0,128,0) if selected == key else BLACK
            surf = small_font.render(f'{key}: {name}  ({desc})', True, color)
            pygame.draw.rect(screen, (200,200,200) if selected == key else (240,240,240), (WIDTH//2-160, 220+idx*70, 320, 50), border_radius=12)
            screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 230 + idx*70))
        info = small_font.render('Press 1, 2, or 3 to choose', True, GRAY)
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 450))
        pygame.display.flip()

    selecting_level = True
    level = 'basic'
    while selecting_level:
        draw_level_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 'basic'
                    selecting_level = False
                elif event.key == pygame.K_2:
                    level = 'intermediate'
                    selecting_level = False
                elif event.key == pygame.K_3:
                    level = 'hard'
                    selecting_level = False
        clock.tick(30)

    game = HangmanGame(level=level)
    input_letter = ''
    message = ''

    # Draw Hangman function
    def draw_hangman(surface, lives, anim=0):
        center_x = WIDTH // 2
        base_y = HEIGHT // 2 + 100
        # Base
        pygame.draw.line(surface, GRAY, (center_x-60, base_y), (center_x+60, base_y), 6)
        # Pole
        pygame.draw.line(surface, GRAY, (center_x-30, base_y), (center_x-30, base_y-175), 6)
        # Top bar
        pygame.draw.line(surface, GRAY, (center_x-30, base_y-175), (center_x+70, base_y-175), 6)
        # Rope
        pygame.draw.line(surface, BLACK, (center_x+70, base_y-175), (center_x+70, base_y-125), 4)
        # Head
        if lives <= 5 or anim > 0:
            pygame.draw.circle(surface, BLACK, (center_x+70, base_y-100), 15, 3)
        # Body
        if lives <= 4 or anim > 5:
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-85), (center_x+70, base_y-45), 3)
        # Arms and legs
        if lives <= 3 or anim > 10:
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-75), (center_x+40, base_y-65), 3)
        if lives <= 2 or anim > 15:
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-75), (center_x+100, base_y-65), 3)
        if lives <= 1 or anim > 20:
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-45), (center_x+50, base_y-15), 3)
        if lives <= 0 or anim > 25:
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-45), (center_x+90, base_y-15), 3)
        # Swing animation
        if lives <= 0 and anim > 0:
            angle = math.sin(anim/5) * 0.2
            pygame.draw.line(surface, BLACK, (center_x+70, base_y-175), 
                             (center_x+70+int(10*math.sin(angle)), base_y-125+int(10*math.cos(angle))), 4)

    # Draw UI
    def draw_ui():
        title = font.render('HANGMAN', True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        # Show current level at the top left
        level_map = {'basic': 'Basic', 'intermediate': 'Intermediate', 'hard': 'Hard'}
        level_display = small_font.render(f'Level: {level_map.get(game.level, game.level).capitalize()}', True, BLACK)
        screen.blit(level_display, (20, 20))
        y_start = HEIGHT - 180
        word_surface = small_font.render(game.get_display_word(), True, BLACK)
        screen.blit(word_surface, (WIDTH//2 - word_surface.get_width()//2, y_start))
        guessed_surface = small_font.render('Guessed: ' + ' '.join(sorted(game.guessed)), True, BLACK)
        screen.blit(guessed_surface, (WIDTH//2 - guessed_surface.get_width()//2, y_start + 30))
        lives_surface = small_font.render(f'Lives: {game.lives}', True, BLACK)
        screen.blit(lives_surface, (WIDTH//2 - lives_surface.get_width()//2, y_start + 60))
        timer_surface = small_font.render(f'Time: {game.timer}', True, BLACK)
        screen.blit(timer_surface, (WIDTH//2 - timer_surface.get_width()//2, y_start + 90))
        input_surface = small_font.render(f'Input: {input_letter}', True, BLACK)
        screen.blit(input_surface, (WIDTH//2 - input_surface.get_width()//2, y_start + 120))

    # Game over screen
    def draw_game_over():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255,255,255,220))
        screen.blit(overlay, (0,0))
        if game.win:
            msg = 'You Win!'
            color = (0, 128, 0)
        else:
            msg = 'Game Over!'
            color = (255, 0, 0)
        msg_surface = font.render(msg, True, color)
        screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, 120))
        ans_surface = small_font.render(f'Answer: {game.get_answer()}', True, BLACK)
        screen.blit(ans_surface, (WIDTH//2 - ans_surface.get_width()//2, 220))
        restart_surface = small_font.render('Press R to restart or Q to quit.', True, BLACK)
        screen.blit(restart_surface, (WIDTH//2 - restart_surface.get_width()//2, 320))

    # -------------------------
    # Main Game Loop
    # -------------------------
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_RETURN and input_letter:
                    game.guess(input_letter)
                    input_letter = ''
                elif event.unicode.isalpha() and len(event.unicode) == 1:
                    input_letter = event.unicode.lower()
            elif event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:
                    game.pick_word()
                    input_letter = ''
                elif event.key == pygame.K_q:
                    running = False

        if not game.game_over:
            game.update_timer()
        else:
            game.animate_hanging()

        draw_hangman(screen, game.lives, game.animation_progress)
        draw_ui()
        if game.game_over:
            draw_game_over()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()
