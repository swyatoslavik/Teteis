import pygame as pg
import random, time, sys
from pygame.locals import *


class Tetris():
    def __init__(self, level, score, window_w, window_h):
        self.level = level
        self.points = score
        self.fps = 25
        self.window_w, self.window_h = window_w, window_h
        self.block, self.cup_h, self.cup_w = 20, 20, 10
        self.side_freq, self.down_freq = 0.15, 0.1
        self.side_margin = int((self.window_w - self.cup_w * self.block) / 2)
        self.top_margin = self.window_h - (self.cup_h * self.block) - 5

        self.colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # синий, зеленый, красный, желтый
        self.lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30),
                            (255, 255, 30))  # светло-синий, светло-зеленый, светло-красный, светло-желтый
        self.white, self.gray, self.black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
        self.brd_color, self.bg_color, self.txt_color, self.title_color, self.info_color = self.white, self.black, self.white, \
                                                                                           self.colors[3], self.colors[
                                                                                               2]

        self.fig_w, self.fig_h = 5, 5
        self.empty = 'o'

        self.figures = {'S': [['ooooo',
                               'ooooo',
                               'ooxxo',
                               'oxxoo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'ooxxo',
                               'oooxo',
                               'ooooo']],
                        'Z': [['ooooo',
                               'ooooo',
                               'oxxoo',
                               'ooxxo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'oxxoo',
                               'oxooo',
                               'ooooo']],
                        'J': [['ooooo',
                               'oxooo',
                               'oxxxo',
                               'ooooo',
                               'ooooo'],
                              ['ooooo',
                               'ooxxo',
                               'ooxoo',
                               'ooxoo',
                               'ooooo'],
                              ['ooooo',
                               'ooooo',
                               'oxxxo',
                               'oooxo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'ooxoo',
                               'oxxoo',
                               'ooooo']],
                        'L': [['ooooo',
                               'oooxo',
                               'oxxxo',
                               'ooooo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'ooxoo',
                               'ooxxo',
                               'ooooo'],
                              ['ooooo',
                               'ooooo',
                               'oxxxo',
                               'oxooo',
                               'ooooo'],
                              ['ooooo',
                               'oxxoo',
                               'ooxoo',
                               'ooxoo',
                               'ooooo']],
                        'I': [['ooxoo',
                               'ooxoo',
                               'ooxoo',
                               'ooxoo',
                               'ooooo'],
                              ['ooooo',
                               'ooooo',
                               'xxxxo',
                               'ooooo',
                               'ooooo']],
                        'O': [['ooooo',
                               'ooooo',
                               'oxxoo',
                               'oxxoo',
                               'ooooo']],
                        'T': [['ooooo',
                               'ooxoo',
                               'oxxxo',
                               'ooooo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'ooxxo',
                               'ooxoo',
                               'ooooo'],
                              ['ooooo',
                               'ooooo',
                               'oxxxo',
                               'ooxoo',
                               'ooooo'],
                              ['ooooo',
                               'ooxoo',
                               'oxxoo',
                               'ooxoo',
                               'ooooo']]}

    def pauseScreen(self):
        pause = pg.Surface((600, 500), pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.display_surf.blit(pause, (0, 0))

    def main(self):
        pg.init()
        self.fps_clock = pg.time.Clock()
        self.display_surf = pg.display.set_mode((self.window_w, self.window_h))
        self.basic_font = pg.font.Font('12568.otf', 25)
        self.big_font = pg.font.Font('12568.otf', 75)
        pg.display.set_caption('Тетрис')
        self.showText('Тетрис')
        while True:
            self.runTetris()
            self.pauseScreen()
            self.showTextRed('Игра окончена')

    def runTetris(self):
        cup = self.emptycup()
        last_move_down = time.time()
        last_side_move = time.time()
        last_fall = time.time()
        going_down = False
        going_left = False
        going_right = False
        level, fall_speed = self.calcSpeed(self.points)
        fallingFig = self.getNewFig()
        nextFig = self.getNewFig()
        while True:
            if self.points == 1 + self.level + ((self.level - 1) * 10):
                from main_menu import MainMenu
                pg.quit()
                main_menu = MainMenu()
                main_menu.start_the_game(True, self.points)
            if fallingFig == None:
                fallingFig = nextFig
                nextFig = self.getNewFig()
                last_fall = time.time()
                if not self.checkPos(cup, fallingFig):
                    from main_menu import MainMenu
                    self.showTextRed("game over")
                    pg.quit()
                    main_menu = MainMenu()
                    main_menu.end_the_game(False, self.points)
            self.quitGame()
            for event in pg.event.get():
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.pauseScreen()
                        self.showText('Пауза')
                        last_fall = time.time()
                        last_move_down = time.time()
                        last_side_move = time.time()
                    elif event.key == K_LEFT:
                        going_left = False
                    elif event.key == K_RIGHT:
                        going_right = False
                    elif event.key == K_DOWN:
                        going_down = False

                elif event.type == KEYDOWN:
                    # перемещение фигуры вправо и влево
                    if event.key == K_LEFT and self.checkPos(cup, fallingFig, adjX=-1):
                        fallingFig['x'] -= 1
                        going_left = True
                        going_right = False
                        last_side_move = time.time()

                    elif event.key == K_RIGHT and self.checkPos(cup, fallingFig, adjX=1):
                        fallingFig['x'] += 1
                        going_right = True
                        going_left = False
                        last_side_move = time.time()

                    # поворачиваем фигуру, если есть место
                    elif event.key == K_UP:
                        fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(self.figures[fallingFig['shape']])
                        if not self.checkPos(cup, fallingFig):
                            fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(
                                self.figures[fallingFig['shape']])

                    # ускоряем падение фигуры
                    elif event.key == K_DOWN:
                        going_down = True
                        if self.checkPos(cup, fallingFig, adjY=1):
                            fallingFig['y'] += 1
                        last_move_down = time.time()

                    # мгновенный сброс вниз
                    elif event.key == K_RETURN:
                        going_down = False
                        going_left = False
                        going_right = False
                        for i in range(1, self.cup_h):
                            if not self.checkPos(cup, fallingFig, adjY=i):
                                break
                        fallingFig['y'] += i - 1

            # управление падением фигуры при удержании клавиш
            if (going_left or going_right) and time.time() - last_side_move > self.side_freq:
                if going_left and self.checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                elif going_right and self.checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                last_side_move = time.time()

            if going_down and time.time() - last_move_down > self.down_freq and self.checkPos(cup, fallingFig, adjY=1):
                fallingFig['y'] += 1
                last_move_down = time.time()

            if time.time() - last_fall > fall_speed:  # свободное падение фигуры
                if not self.checkPos(cup, fallingFig, adjY=1):  # проверка "приземления" фигуры
                    self.addToCup(cup, fallingFig)  # фигура приземлилась, добавляем ее в содержимое стакана
                    self.points += self.clearCompleted(cup)
                    level, fall_speed = self.calcSpeed(self.points)
                    fallingFig = None
                else:  # фигура пока не приземлилась, продолжаем движение вниз
                    fallingFig['y'] += 1
                    last_fall = time.time()

            # рисуем окно игры со всеми надписями
            self.display_surf.fill(self.bg_color)
            self.drawTitle()
            self.gamecup(cup)
            self.drawInfo(self.points, level)
            self.drawnextFig(nextFig)
            if fallingFig != None:
                self.drawFig(fallingFig)
            pg.display.update()
            self.fps_clock.tick(self.fps)

    def txtObjects(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def stopGame(self):
        from main_menu import MainMenu
        pg.quit()
        main_menu = MainMenu()
        main_menu.end_the_game(True, self.points)

    def checkKeys(self):
        self.quitGame()

        for event in pg.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    def showText(self, text):
        titleSurf, titleRect = self.txtObjects(text, self.big_font, self.title_color)
        titleRect.center = (int(self.window_w / 2) - 3, int(self.window_h / 2) - 40)
        self.display_surf.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = self.txtObjects('Нажмите любую клавишу для продолжения', self.basic_font,
                                                     self.title_color)
        pressKeyRect.center = (int(self.window_w / 2), int(self.window_h / 2) + 30)
        self.display_surf.blit(pressKeySurf, pressKeyRect)

        while self.checkKeys() == None:
            pg.display.update()
            self.fps_clock.tick()

    def showTextRed(self, text):
        titleSurf, titleRect = self.txtObjects(text, self.big_font, self.info_color)
        titleRect.center = (int(self.window_w / 2) - 3, int(self.window_h / 2) - 40)
        self.display_surf.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = self.txtObjects('Нажмите любую клавишу для продолжения', self.basic_font,
                                                     self.info_color)
        pressKeyRect.center = (int(self.window_w / 2), int(self.window_h / 2) + 30)
        self.display_surf.blit(pressKeySurf, pressKeyRect)

        while self.checkKeys() == None:
            pg.display.update()
            self.fps_clock.tick()

    def quitGame(self):
        for _ in pg.event.get(QUIT):  # проверка всех событий, приводящих к выходу из игры
            self.stopGame()
        for event in pg.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.stopGame()
            pg.event.post(event)

    def calcSpeed(self, points):
        # вычисляет уровень
        level = int(points / 10) + 1
        fall_speed = 0.27 - (level * 0.05)
        return level, fall_speed

    def getNewFig(self):
        # возвращает новую фигуру со случайным цветом и углом поворота
        shape = random.choice(list(self.figures.keys()))
        newFigure = {'shape': shape,
                     'rotation': random.randint(0, len(self.figures[shape]) - 1),
                     'x': int(self.cup_w / 2) - int(self.fig_w / 2),
                     'y': -2,
                     'color': random.randint(0, len(self.colors) - 1)}
        return newFigure

    def addToCup(self, cup, fig):
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                if self.figures[fig['shape']][fig['rotation']][y][x] != self.empty:
                    cup[x + fig['x']][y + fig['y']] = fig['color']

    def emptycup(self):
        # создает пустой стакан
        cup = []
        for i in range(self.cup_w):
            cup.append([self.empty] * self.cup_h)
        return cup

    def incup(self, x, y):
        return x >= 0 and x < self.cup_w and y < self.cup_h

    def checkPos(self, cup, fig, adjX=0, adjY=0):
        # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                abovecup = y + fig['y'] + adjY < 0
                if abovecup or self.figures[fig['shape']][fig['rotation']][y][x] == self.empty:
                    continue
                if not self.incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                    return False
                if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != self.empty:
                    return False
        return True

    def isCompleted(self, cup, y):
        # проверяем наличие полностью заполненных рядов
        for x in range(self.cup_w):
            if cup[x][y] == self.empty:
                return False
        return True

    def clearCompleted(self, cup):
        # Удаление заполенных рядов и сдвиг верхних рядов вниз
        removed_lines = 0
        y = self.cup_h - 1
        while y >= 0:
            if self.isCompleted(cup, y):
                for pushDownY in range(y, 0, -1):
                    for x in range(self.cup_w):
                        cup[x][pushDownY] = cup[x][pushDownY - 1]
                for x in range(self.cup_w):
                    cup[x][0] = self.empty
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    def convertCoords(self, block_x, block_y):
        return (self.side_margin + (block_x * self.block)), (self.top_margin + (block_y * self.block))

    def drawBlock(self, block_x, block_y, color, pixelx=None, pixely=None):
        # отрисовка квадратных блоков, из которых состоят фигуры
        if color == self.empty:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertCoords(block_x, block_y)
        pg.draw.rect(self.display_surf, self.colors[color], (pixelx + 1, pixely + 1, self.block - 1, self.block - 1), 0,
                     3)

    def gamecup(self, cup):
        # граница игрового поля-стакана
        pg.draw.rect(self.display_surf, self.brd_color,
                     (self.side_margin - 4, self.top_margin - 4, (self.cup_w * self.block) + 8,
                      (self.cup_h * self.block) + 8),
                     5)

        # фон игрового поля
        pg.draw.rect(self.display_surf, self.bg_color,
                     (self.side_margin, self.top_margin, self.block * self.cup_w, self.block * self.cup_h))
        for x in range(self.cup_w):
            for y in range(self.cup_h):
                self.drawBlock(x, y, cup[x][y])

    def drawTitle(self):
        titleSurf = self.big_font.render('Тетрис', True, self.title_color)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (self.window_w - 355, 5)
        self.display_surf.blit(titleSurf, titleRect)

    def drawInfo(self, points, level):
        pointsSurf = self.basic_font.render(f'Баллы: {points}', True, self.txt_color)
        pointsRect = pointsSurf.get_rect()
        pointsRect.topleft = (self.window_w - 480, 180)
        self.display_surf.blit(pointsSurf, pointsRect)

        levelSurf = self.basic_font.render(f'Уровень: {level}', True, self.txt_color)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (self.window_w - 480, 250)
        self.display_surf.blit(levelSurf, levelRect)

        pausebSurf = self.basic_font.render('space', True, self.title_color)
        pausebRect = pausebSurf.get_rect()
        pausebRect.topleft = (self.window_w - 67, 455)
        self.display_surf.blit(pausebSurf, pausebRect)

        pausebSurf = self.basic_font.render('Пауза:', True, self.txt_color)
        pausebRect = pausebSurf.get_rect()
        pausebRect.topleft = (self.window_w - 135, 455)
        self.display_surf.blit(pausebSurf, pausebRect)

        escbSurf = self.basic_font.render('Esc', True, self.info_color)
        escbRect = escbSurf.get_rect()
        escbRect.topleft = (self.window_w - 410, 455)
        self.display_surf.blit(escbSurf, escbRect)

        escbSurf = self.basic_font.render('Выход:', True, self.txt_color)
        escbRect = escbSurf.get_rect()
        escbRect.topleft = (self.window_w - 488, 455)
        self.display_surf.blit(escbSurf, escbRect)

    def drawFig(self, fig, pixelx=None, pixely=None):
        figToDraw = self.figures[fig['shape']][fig['rotation']]
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertCoords(fig['x'], fig['y'])

        # отрисовка элементов фигур
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                if figToDraw[y][x] != self.empty:
                    self.drawBlock(None, None, fig['color'], pixelx + (x * self.block), pixely + (y * self.block))

    def drawnextFig(self, fig):  # превью следующей фигуры
        nextSurf = self.basic_font.render('Следующая:', True, self.txt_color)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (self.window_w - 135, 180)
        self.display_surf.blit(nextSurf, nextRect)
        self.drawFig(fig, pixelx=self.window_w - 120, pixely=220)
