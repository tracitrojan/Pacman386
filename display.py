import pygame
import math


class Display:
    def __init__(self, screen, pman):
        self.yellow = (225, 225, 0)
        self.white = (225, 225, 225)
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.font1 = pygame.font.SysFont("comicsansms", 40)
        self.font2 = pygame.font.SysFont("comicsansms", 40)

        self.score = self.font.render("SCORE: ", True, self.white)
        self.score_button = self.score.get_rect()
        self.score_button.centerx = screen.get_rect().centerx - 240
        self.score_button.centery = screen.get_rect().centery + 330

        self.s = self.font.render(str(pman.score), True, self.yellow)
        self.s_button = self.s.get_rect()
        self.s_button.left = screen.get_rect().centerx - 180
        self.s_button.centery = screen.get_rect(). centery + 330

        self.lives = self.font.render("LIVES: ", True, self.white)
        self.lives_button = self.lives.get_rect()
        self.lives_button.centerx = screen.get_rect().centerx + 20
        self.lives_button.centery = screen.get_rect().centery + 330

        self.live = self.font.render(str(pman.lives), True, self.yellow)
        self.live_button = self.live.get_rect()
        self.live_button.centerx = screen.get_rect().centerx + 80
        self.live_button.centery = screen.get_rect().centery + 330

        self.ready = self.font.render("GET READY!", True, self.white)
        self.ready_button = self.ready.get_rect()
        self.ready_button.centerx = screen.get_rect().centerx
        self.ready_button.centery = screen.get_rect().centery + 8

        self.play = self.font1.render("PLAY AGAIN", True, self.white)
        self.play_button = self.play.get_rect()
        self.play_button.centerx = screen.get_rect().centerx + 20
        self.play_button.centery = screen.get_rect().centery - 73

        self.go = self.font.render("GAME OVER", True, self.white)
        self.go_button = self.go.get_rect()
        self.go_button.centerx = screen.get_rect().centerx
        self.go_button.centery = screen.get_rect().centery + 8

        self.pmam = self.font2.render("PACMAN", True, self.white)
        self.pman_button = self.pmam.get_rect()
        self.pman_button.centerx = screen.get_rect().centerx
        self.pman_button.centery = screen.get_rect().centery - 300

        self.ply = self.font.render("PLAY", True, self.yellow)
        self.ply_button = self.play.get_rect()
        self.play_button.centerx = screen.get_rect().centerx + 50
        self.play_button.centery = screen.get_rect().centery + 300

        self.high = self.font.render("High Score: 1000", True, self.white)
        self.high_button = self.high.get_rect()
        self.high_button.centerx = screen.get_rect().centerx
        self.high_button.centery = screen.get_rect().centery + 350

        self.intro = pygame.image.load('images/1.png')
        self.intro = pygame.transform.scale(self.intro, (600, 357))
        self.intro_button = self.intro.get_rect()
        self.intro_button.centerx = screen.get_rect().centerx
        self.intro_button.centery = screen.get_rect().centery - 100
        self.index = 1

    def start(self, screen, stats):
        self.high = self.font.render("High Score: " + str(stats.high_score), True, self.white)
        screen.fill((0, 0, 0))
        screen.blit(self.ply, self.play_button)
        screen.blit(self.high, self.high_button)

        if self.index > 83:
            self.index = 1
        else:
            self.index += .1

        file = "images/" + str(math.floor(self.index)) + ".png"
        self.intro = pygame.image.load(file)
        self.intro = pygame.transform.scale(self.intro, (600, 357))
        screen.blit(self.intro, self.intro_button)

    def button_clicks(self, pman, stats, maze):
        play_clicked = self.play_button.collidepoint(pygame.mouse.get_pos())
        if play_clicked and stats.game_over:
            pman.lives = 3
            pman.score = 0
            stats.game_over = False
            maze.build()

        ply_clicked = self.play_button.collidepoint(pygame.mouse.get_pos())
        if ply_clicked and stats.start_screen:
            stats.start_screen = False

    def score_blit(self, screen, stats, pman):
        self.s = self.font.render(str(pman.score), True, self.yellow)
        self.live = self.font.render(str(pman.lives), True, self.yellow)

        screen.blit(self.score, self.score_button)
        screen.blit(self.s, self.s_button)
        screen.blit(self.lives, self.lives_button)
        screen.blit(self.live, self.live_button)

        if stats.get_ready and not stats.game_over:
            screen.blit(self.ready, self.ready_button)

        if stats.game_over:
            screen.blit(self.go, self.go_button)
            screen.blit(self.play, self.play_button)
