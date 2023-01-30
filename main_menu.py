import pygame
import pygame_menu
import sqlite3
from snake import Snake
from tetris import Tetris




class MainMenu():
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 400))
        self.username = '1'
        self.info_from_bd = self.get_info_from_bd()

    def start_the_game(self, flag=False):
        res = self.get_info_from_bd()
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        if res[3] == 'Tetris':
            if flag:
                cursor.execute("UPDATE users SET last_game = ? WHERE usid = ?", ("Snake", int(self.username)))
                conn.commit()
                conn.close()
                snake = Snake(res[2], res[4], 500, 500)
                snake.play()
            else:
                cursor.execute("UPDATE users SET last_game = ? WHERE usid = ?", ("Tetris", int(self.username)))
                conn.commit()
                conn.close()
                tetris = MiniTetris(res[2], res[4], 500, 500)
                tetris.play()
        elif res[3] == 'Snake':
            if flag:
                cursor.execute("UPDATE users SET last_game = ? WHERE usid = ?", ("Tetris", int(self.username)))
                conn.commit()
                conn.close()
                tetris = MiniTetris(res[2], res[4], 500, 500)
                tetris.play()
            else:
                cursor.execute("UPDATE users SET last_game = ? WHERE usid = ?", ("Snake", int(self.username)))
                conn.commit()
                conn.close()
                snake = Snake(res[2], res[4], 500, 500)
                snake.play()
        else:
            cursor.execute("UPDATE users SET last_game = ? WHERE usid = ?", ("Tetris", int(self.username)))
            conn.commit()
            conn.close()
            tetris = MiniTetris(res[2], res[4], 500, 500)
            tetris.play()

    def end_the_game(self, flag=False, score=0):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        if flag:
            cursor.execute("UPDATE users SET last_score = ? WHERE usid = ?", (score, int(self.username)))
            conn.commit()
            conn.close()
        else:
            cursor.execute("UPDATE users SET last_score = ? WHERE usid = ?", (0, int(self.username)))
        quit()

    def rules(self):
        pass

    def get_info_from_bd(self):
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE usid = ?", (int(self.username),))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO users (usid) VALUES (?)", (int(self.username),))
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE usid = ?", (int(self.username),))
            result = cursor.fetchone()
        conn.close()
        return result

    def change_user(self, _, difficulty):
        self.username = difficulty
        self.info_from_bd = self.get_info_from_bd()

    def main(self):
        menu = pygame_menu.Menu('Добро пожаловать!', 400, 300,
                                theme=pygame_menu.themes.THEME_SOLARIZED)

        menu.add.selector('Игрок :', [('1', 1)], onchange=self.change_user)
        menu.add.button('Играть', self.start_the_game)
        menu.add.button('Правила', self.rules)
        menu.add.button('Выйти', pygame_menu.events.EXIT)

        menu.mainloop(self.surface)


class MiniTetris():
    def __init__(self, level, score, win_x=500, win_y=500):
        self.level = level
        self.score = score
        self.win_x = win_x
        self.win_y = win_y

    def play(self):
        tetris = Tetris(self.level, self.score, self.win_x, self.win_y)
        tetris.main()


class MiniSnake():
    def __init__(self, level, score, win_x=500, win_y=500):
        self.level = level
        self.score = score
        self.win_x = win_x
        self.win_y = win_y

    def play(self):
        snake = Snake(self.level, self.score, self.win_x, self.win_y)
        snake.play()


if "__main__" == __name__:
    main = MainMenu()
    main.main()
