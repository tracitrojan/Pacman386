import pygame as pg
import math
import random
from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector
from timer import Timer, TimerDual
from imagerect import ImageRect


class Ghost(Sprite):
    SPEED = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.velocity = Ghost.SPEED * Vector(1, 0)

        self.image = pg.image.load('images/red_ghost4r.png')
        self.rect = self.image.get_rect()

        self.rect.left = self.rect.width
        self.rect.top = self.rect.height
        self.x = float(self.rect.x)
        self.alive = True
        self.rev = False
        self.timer = None
        self.timerR = None
        self.timerL = None
        self.timerU = None
        self.timerD = None
        self.current_direction = 'right'

        self.eyes_animations = {
            'left': 'eyes_left', 'down': 'eyes_down', 'right': 'eyes_right', 'up': 'eyes_up'
        }
        self.timerBlueGhost = TimerDual(game=self.game, images1=['g3762', 'g3770'], images2=['g3512', 'g3520'], wait1=200,
                    wait2=200, wait_switch_timers=6000, frameindex1=0, frameindex2=0, step1=1, step2=1, looponce=False)

    def width(self): return self.rect.width

    def height(self): return self.rect.height

    def check_edges(self):
        r = self.rect
        s_r = self.screen.get_rect()
        return r.right >= s_r.right or r.left <= 0

    def draw(self):
        temp_image = self.timer.imagerect()
        self.screen.blit(temp_image.image, self.rect)

    def move(self):
        if self.velocity == Vector():
            return

        self.ai()

        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)
        # change = False


        '''
        wall_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)
        if len(wall_hit_list) > 0:
            self.rect.left -= self.velocity.x
            self.rect.top -= self.velocity.y
            # change direction
            self.ai()
            '''

        if self.alive and not self.rev:
            if self.velocity.x != 0:
                if self.velocity.x > 0:
                    self.current_direction = 'right'
                    self.timer = self.timerR
                else:
                    self.current_direction = 'left'
                    self.timer = self.timerL
            elif self.velocity.y != 0:
                if self.velocity.y > 0:
                    self.current_direction = 'down'
                    self.timer = self.timerD
                else:
                    self.current_direction = 'up'
                    self.timer = self.timerU
        elif self.alive and self.rev:
            # call run away functionality
            pass
        else:  # eyes
            # call eyes run to start
            pass

    def reverse_draw(self):
        # self.timer = self.timerBlueGhost
        if not self.alive:
            # eyes
            # temp_image = self.eyes_animations[self.current_direction]
            temp_image = (ImageRect(self.screen, self.eyes_animations[self.current_direction], height=25, width=25))
            self.screen.blit(temp_image.image, self.rect)
            return
        if self.timerBlueGhost.counter >= 2:
            self.reanimate()
        temp_image = self.timer.imagerect()
        self.screen.blit(temp_image.image, self.rect)

    def reverse(self):
        self.rev = True
        self.timer = self.timerBlueGhost
        self.timerBlueGhost.reset()

    def reanimate(self):
        self.rev = False
        self.alive = True
        # self.reset()
        self.timer = self.timerD

    def update(self):
        pass
        # self.move()
        # self.draw()

    def reverse_update(self):
        self.move()
        self.reverse_draw()

    def reset(self):
        self.timer = self.timerD
        self.rev = False
        self.alive = True

    def update(self):
        if self.rev:
            self.reverse_update()
            return
        self.move()
        self.draw()

    def ai(self):
        pass


class RedGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['red_ghost3r', 'red_ghost4r'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerD = Timer(game=self.game, images=['red_ghost3d', 'red_ghost4d'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerL = Timer(game=self.game, images=['red_ghost3l', 'red_ghost4l'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerU = Timer(game=self.game, images=['red_ghost3u', 'red_ghost4u'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timer = self.timerU
        self.current_direction = 'up'

    def ai(self):
        # write functionality of movement here
        x_c = self.velocity  # x choice
        y_c = self.velocity  # y choice
        choice = self.velocity

        wall_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)
        if len(wall_hit_list) > 0:
            self.rect.left -= self.velocity.x
            self.rect.top -= self.velocity.y

        delta_x = self.x - self.game.pacman.x
        delta_y = self.y - self.game.pacman.y

        if self.current_direction == 'right' or self.current_direction == 'left':
            if delta_x == 0 or len(wall_hit_list) > 0:
                # change y
                if delta_y > 0:
                    choice = self.SPEED * Vector(0, -1)
                elif delta_y < 0:
                    choice = self.SPEED * Vector(0, 1)
                else:
                    choice = Vector(0, 0)
        else:
            if delta_y == 0 or len(wall_hit_list) > 0:
                # change x
                if delta_x > 0:
                    choice = self.SPEED * Vector(-1, 0)
                elif delta_x < 0:
                    choice = self.SPEED * Vector(1, 0)
                else:
                    choice = Vector(0, 0)
        self.velocity = choice


class PinkGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8200', 'g3168'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8191', 'g3139'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8269', 'g3159'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g2727', 'g3284'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timer = self.timerU
        self.current_direction = 'up'

        self.moveD = "u"
        self.directions_remain = []
        # self.alive = True
        # self.eat = False   # same as self.rev

    def ai(self):
        # write functionality of movement here
        self.self_movement()
        if self.current_direction == 'u':
            self.velocity = Vector(0, -1)
        elif self.current_direction == 'd':
            self.velocity = Vector(0, 1)
        elif self.current_direction == 'l':
            self.velocity = Vector(-1, 0)
        elif self.currect_direction == 'r':
            self.velocity = Vector(1, 0)

    def ball_stop(self):
        if self.moveD == "l":
            temp = self.rect.move(-1, 0)
        elif self.moveD == "r":
            temp = self.rect.move(1, 0)
        elif self.moveD == "u":
            temp = self.rect.move(0, -1)
        elif self.moveD == "d":
            temp = self.rect.move(0, 1)
        else:
            temp = self.rect.move(0, 0)

        # for wall in self.game.walls:
        # if wall.rect.colliderect(temp):
        # if pg.sprite.spritecollideany(temp, self.game.walls):
        t = temp.collidelist(self.game.walls)
        if t > 0:
            return True

        return False

    def self_movement(self):
        if self.moveD == "u" and self.rect == (300, 230, 30, 30):
            self.moveD = "l"

        elif 295 < self.rect.x < 305 and 325 < self.rect.y < 335:
            self.moveD = "u"

        if self.ball_stop() is True and self.rev is False:
            self.check_directions()
            if len(self.directions_remain) == 0:
                self.moveD = "l"
                self.moveD = "r"
                self.moveD = "u"
                self.moveD = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.moveD = rand

        if self.rev is True:
            self.check_directions()

            if self.rect.x < 190 and self.rect.y is not 230:
                if "r" in self.directions_remain:
                    self.moveD = "r"
                elif self.ball_stop():
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.x > 410 and self.rect.y is not 230:
                if "l" in self.directions_remain:
                    self.moveD = "l"
                elif self.ball_stop():
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y < 230 and self.rect.x is not 300:
                if "d" in self.directions_remain:
                    self.moveD = "d"
                elif self.ball_stop():
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y > 230 and self.rect.x is not 300:
                if "u" in self.directions_remain:
                    self.moveD = "u"
                elif self.ball_stop():
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y is 230 and 190 < self.rect.x < 410:
                if 295 < self.rect.x < 305:
                    self.moveD = "d"
                elif self.rect.x < 300:
                    self.moveD = "r"
                elif self.rect.x > 300:
                    self.moveD = "l"
            else:
                rand = random.choice(self.directions_remain)
                self.moveD = rand
        self.current_direction = self.moveD

    def check_directions(self):
        self.directions_remain.clear()
        self.current_direction = "up"
        if self.ball_stop() is False:
            if self.moveD is not "d":
                self.directions_remain.append("u")

        self.current_direction = "down"
        if self.ball_stop() is False:
            if self.moveD is not "u":
                self.directions_remain.append("d")

        self.current_direction = "left"
        if self.ball_stop() is False:
            if self.moveD is not "r":
                self.directions_remain.append("l")

        self.current_direction = "right"
        if self.ball_stop() is False:
            if self.moveD is not "l":
                self.directions_remain.append("r")

    # def blitme(self):
    # self.image.blitme()

    def dead_collide(self, pm, maze):
        if pg.sprite.collide_rect(self, pm) and self.alive is False:
            if self.alive is False and self.eat is False:
                pm.score += 200
                eat = pg.mixer.Sound('sounds/eatghost.wav')
                eat.play()
                self.rev = True

        if self.eat is True:
            for lines in maze.lines:
                if lines.colliderect(self):
                    self.rev = False
                    self.alive = True


class BlueGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8230', 'g8357'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8162', 'g3112'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8240', 'g3222'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g3040', 'g6234'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timer = self.timerR
        self.current_direction = 'right'

    def ai(self):
        # write functionality of movement here
        pass


class OrangeGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8220', 'g8348'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8172', 'g3121'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8250', 'g3195'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g3027', 'g6119'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timer = self.timerL
        self.current_direction = 'left'

    def ai(self):
        # write functionality of movement here
        pass


class Haunt:
    SPEED = 0

    def __init__(self, game):
        self.ghosts = pg.sprite.Group()
        self.game = game
        self.ghost_dies = pg.mixer.Sound("sounds/pacman_eatghost.wav")
        ghost = Ghost(game=self.game)
        self.velocity = Haunt.SPEED * Vector(1, 0)

        self.g_color = {
            'r': RedGhost, 'p': PinkGhost, 'b': BlueGhost, 'o': OrangeGhost
        }

        # self.create_ghost(self.game.ghost_start[0], 'r')
        self.create_ghost(self.game.ghost_start[2], 'p')
        # self.create_ghost(self.game.ghost_start[1], 'b')
        # self.create_ghost(self.game.ghost_start[3], 'o')

    def create_ghost(self, n, r):
        ghost = self.g_color[r](game=self.game)

        rect = ghost.rect
        width, height = rect.size
        # ghost.x = width + 2 * n * width  # controls location
        ghost.x = n[0]
        ghost.y = n[1]
        rect.x = ghost.x
        rect.y = ghost.y
        # rect.y = rect.height + 2 * height * row
        self.ghosts.add(ghost)

    def check_sides(self):
        for ghost in self.ghosts.sprites():
            if ghost.check_edges():
                self.change_ghost_direction()
                break

    def check_bottom(self):
        for ghost in self.ghosts.sprites():
            if ghost.rect.bottom > self.game.HEIGHT:
                pass
                # self.game.restart()

    def check_pacman_hit(self):
        temp = pg.sprite.spritecollideany(self.game.pacman, self.ghosts)
        if temp:
            # self.game.restart()
            if temp.rev and temp.alive:
                temp.alive = False
                pg.mixer.Sound.play(self.ghost_dies)
                temp.animation_num = 'eyes'
                # temp.reanimate()  # CHANGE LATER
                print('ghost hit: change to eyes')
                self.game.score += 20  # CHANGE THIS NUMBER LATER
            elif not temp.rev:
                pg.mixer.Sound.play(self.game.pacman.pacman_dies)
                self.frozen()
                self.game.pacman.alive = False
                self.game.pacman.timer = self.game.pacman.timerPacmanDeath
                self.game.pacman.timerPacmanDeath.reset()
                # self.game.pacman.death()
            return

    def change_ghost_direction(self):
        for ghost in self.ghosts.sprites():
            ghost.rect.y += self.game.GHOST_DROP
            ghost.velocity.x *= -1.1

    def frozen(self):
        for ghost in self.ghosts.sprites():
            ghost.velocity.x = 0
            ghost.velocity.y = 0

    def update(self):
        self.check_sides()
        self.check_bottom()

        if self.game.pacman.alive:
            self.check_pacman_hit()
        self.ghosts.update()

    def reverse(self):
        for ghost in self.ghosts:
            ghost.reverse()
