import pygame
import pygame_menu

from snake import Snake
from tetris2 import Tetris

pygame.init()
surface = pygame.display.set_mode((600, 400))




# def set_difficulty(value, difficulty):
#     pass

def start_the_game():
    if GAME == "Tetris":
        GAME = "Snake"
        snake = Snake(LEVEL, 500, 500)
        snake.play()
    else:
        GAME = "Tetris"
        tetris = Tetris(500, 500)
        tetris.main()


def rules():
    pass

def get_info_from_bd(username):
    import sqlite3
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        conn.close()
def main():
    menu = pygame_menu.Menu('Добро пожаловать!', 400, 300,
                            theme=pygame_menu.themes.THEME_SOLARIZED)

    menu.add.text_input('Имя: ', default='Неизвестный', onreturn=get_info_from_bd)
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Правила', rules)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(surface)

if "__main__" == __name__:
    main()