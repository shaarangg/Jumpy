from os import close
import pygame
from pygame.display import set_palette

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy")


# Setting frame rate
FPS = 60
clock=pygame.time.Clock()


# Game Variables
GRAVITY = 1


# Define colours
WHITE = (255,255,255)

# Load Assets
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
player_image = pygame.image.load('assets/jump.png').convert_alpha()


# Player class
class Player():
    def __init__(self, x,y):
        self.image = pygame.transform.scale(player_image,(45,45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = (x,y)
        self.flip = False
        self.vel_y=0
    
    def move(self):
        dx=0
        dy=0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.flip=True
            dx-=10
        if key[pygame.K_d]:
            self.flip=False
            dx+=10

        # Gravity
        self.vel_y += GRAVITY
        dy+=self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy=0
            self.vel_y = -20
            
        self.rect.x+=dx
        self.rect.y+=dy


    def draw(self):
        screen.blit( pygame.transform.flip(self.image,self.flip,False), (self.rect.x - 10,self.rect.y - 5))   
        pygame.draw.rect(screen,WHITE,self.rect,2)

jumpy = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)

run =True
while run:
    screen.blit(bg_image,(0,0))
    clock.tick(FPS)
    jumpy.move()
    jumpy.draw()

    # Event Handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()