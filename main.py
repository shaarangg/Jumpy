import pygame
import random

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
MAX_PLATFORMS = 10

# Define colours
WHITE = (255,255,255)

# Load Assets
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
player_image = pygame.image.load('assets/jump.png').convert_alpha()
platform_image = pygame.image.load('assets/wood.png').convert_alpha()


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



        # Colissions with boundary
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right


        # Colissions with platforms
        for platform in platform_group:
            if(platform.rect.colliderect(self.rect.x,self.rect.y +dy, self.width, self.height)):
                if self.vel_y >0:
                    self.rect.bottom = platform.rect.top
                    dy=0
                    self.vel_y = -20
        # Collissions with ground
        
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy=0
            self.vel_y = -20
        

        self.rect.x+=dx
        self.rect.y+=dy


    def draw(self):
        screen.blit( pygame.transform.flip(self.image,self.flip,False), (self.rect.x - 10,self.rect.y - 5))   
        pygame.draw.rect(screen,WHITE,self.rect,2)


class Platform(pygame.sprite.Sprite):
    def __init__(self,width,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Player instance
jumpy = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)


# Platform
platform_group = pygame.sprite.Group()

for p in range(MAX_PLATFORMS):
    p_w = random.randint(40,60)
    p_x = random.randint(0,SCREEN_WIDTH-p_w)
    p_y = p*random.randint(80,120)
    platform = Platform(p_w,p_x,p_y)
    platform_group.add(platform)

run =True
while run:
    screen.blit(bg_image,(0,0))
    clock.tick(FPS)

    platform_group.draw(screen)

    jumpy.move()
    jumpy.draw()

    # Event Handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()