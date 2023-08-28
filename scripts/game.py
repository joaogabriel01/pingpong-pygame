import pygame
from scripts.obj import Obj
from scripts.scene import Scene
import scripts.settings

WIDTH = 1280
HEIGHT = 720

class Player(Obj):
    def __init__(self, image_path, initial_pos):
        super().__init__(image_path)
        self.rect.topleft = initial_pos
        self.velocidade = 0

    def limit(self):
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height

class Ball(Obj):
    def __init__(self, image_path, initial_dir):
        super().__init__(image_path)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.dir_x, self.dir_y = initial_dir

    def move(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.rect.height:
            self.dir_y *= -1

class Game(Scene):
    def __init__(self):
        super().__init__()


        self.bg = Obj("assets/bg.png")
        self.player1 = Player("assets/player1.png", (0, (HEIGHT // 2) - 71))
        self.player2 = Player("assets/player2.png", (WIDTH - 109, (HEIGHT // 2) - 71))
        self.ball = Ball("assets/ball.png", (6, 6))

        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, 50)

        self.fade_img = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.fade = self.fade_img.get_rect()
        self.fade_img.fill((0, 0, 0))
        self.fade_alpha = 255

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.player1.velocidade = 6
            elif event.key == pygame.K_w:
                self.player1.velocidade = -6

    def update(self):
    
        self.player1.rect.y += self.player1.velocidade
        self.player1.limit()

    
        self.player2.rect.y = self.ball.rect.y - self.player2.rect.height / 2
        self.player2.limit()

        self.ball.move() 

    
        if self.ball.rect.colliderect(self.player1.rect) or self.ball.rect.colliderect(self.player2.rect):
            self.ball.dir_x *= -1

    
        if self.ball.rect.x <= 0:
            self.player2_score += 1
            self.ball.rect.centerx = WIDTH / 2
            self.ball.dir_x *= -1
        elif self.ball.rect.x >= WIDTH:
            self.player1_score += 1
            self.ball.rect.centerx = WIDTH / 2
            self.ball.dir_x *= -1

    
        if self.player1_score >= 3 or self.player2_score >= 3:
            self.active = False

    
        if self.fade_alpha > 0:
            self.fade_alpha -= 10

    def draw(self):
    
        self.display.fill((0, 0, 0))

    
        self.display.blit(self.bg.image, self.bg.rect)

    
        self.display.blit(self.player1.image, self.player1.rect)
        self.display.blit(self.player2.image, self.player2.rect)
        self.display.blit(self.ball.image, self.ball.rect)

    
        placar_player1 = self.font.render(str(self.player1_score), True, (255, 255, 255))
        placar_player2 = self.font.render(str(self.player2_score), True, (255, 255, 255))
        self.display.blit(placar_player1, (500, 50))
        self.display.blit(placar_player2, (780, 50))

    
        if self.fade_alpha > 0:
            self.fade_img.set_alpha(self.fade_alpha)
            self.display.blit(self.fade_img, self.fade)
