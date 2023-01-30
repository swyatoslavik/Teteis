import pygame
import sys
import random


COLORS = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # синий, зеленый, красный, желтый
LIGHTCOLORS = ((30, 30, 255), (50, 255, 50), (255, 30, 30),
               (255, 255, 30))  # светло-синий, светло-зеленый, светло-красный, светло-желтый
ALL_COLORS = COLORS + LIGHTCOLORS
WINDOW_X, WINDOW_Y = 500, 500
SPEED = 10


def get_random_color():
    return ALL_COLORS[random.randint(0, len(ALL_COLORS) - 1)]


class Fruit():
    def __init__(self):
        self.window_x = WINDOW_X
        self.window_y = WINDOW_Y
        self.position = [random.randrange(1, (self.window_x // 10)) * 10,
                         random.randrange(1, (self.window_y // 10)) * 10]
        self.color = get_random_color()

    def get_info(self):
        return self.position, self.color


class Snake:
    def __init__(self, level, score, window_x, window_y):
        self.level = level
        self.score = score
        self.snake_speed = 10
        self.window_x = window_x
        self.window_y = window_y
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        pygame.init()
        pygame.display.set_caption('Змейка')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50],
                           [90, 50],
                           [80, 50],
                           [70, 50]]
        self.snake_colors = [get_random_color(),
                             get_random_color(),
                             get_random_color(),
                             get_random_color()]
        fruit = Fruit()
        self.fruit = fruit.get_info()
        self.fruit_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.die = False
    def show_score(self, _, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Раунд : ' + str(self.level) + '\nСчёт: ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        self.game_window.blit(score_surface, score_rect)


    def game_over(self):
        self.snake_speed = 0
        # my_font = pygame.font.SysFont('times new roman', 50)
        # game_over_surface = my_font.render('Результат : ' + str(self.score), True, COLORS[2])
        # game_over_rect = game_over_surface.get_rect()
        # game_over_rect.midtop = (self.window_x / 2, self.window_y / 4)
        # self.game_window.blit(game_over_surface, game_over_rect)
        # pygame.display.flip()
        from main_menu import MainMenu
        pygame.quit()
        main_menu = MainMenu()
        main_menu.end_the_game()

    def play(self):
        while True:
            if self.score == 8 + self.level * 2:
                from main_menu import MainMenu
                pygame.quit()
                main_menu = MainMenu()
                main_menu.start_the_game(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    from main_menu import MainMenu
                    pygame.quit()
                    main_menu = MainMenu()
                    main_menu.end_the_game(True, self.score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'
            if self.direction == 'UP':
                self.snake_position[1] -= self.snake_speed
            if self.direction == 'DOWN':
                self.snake_position[1] += self.snake_speed
            if self.direction == 'LEFT':
                self.snake_position[0] -= self.snake_speed
            if self.direction == 'RIGHT':
                self.snake_position[0] += self.snake_speed
            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.fruit[0][0] and self.snake_position[1] == self.fruit[0][1]:
                self.score += 1
                self.fruit_spawn = False
                self.snake_colors.insert(0, self.fruit[1])
            else:
                self.snake_body.pop()
            if not self.fruit_spawn:
                fruit = Fruit()
                self.fruit = fruit.get_info()
            self.fruit_spawn = True
            self.game_window.fill(self.black)
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.snake_colors[self.snake_body.index(pos)],
                                 pygame.Rect(pos[0], pos[1], 10, 10))

            pygame.draw.rect(self.game_window, self.fruit[1],
                             pygame.Rect(self.fruit[0][0], self.fruit[0][1], 10, 10))

            if self.snake_position[0] > self.window_x - self.snake_speed or self.snake_position[0] < 0:
                self.game_over()
            if self.snake_position[1] > self.window_y - self.snake_speed or self.snake_position[1] < 0:
                self.game_over()

            for block in self.snake_body[1:]:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    self.game_over()

            self.show_score(1, self.white, 'times new roman', 20)
            pygame.display.update()
            self.fps.tick(8 + (2 * self.level))

