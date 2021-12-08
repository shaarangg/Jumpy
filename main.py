import pygame
import random
import os

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
SCROLL_THRESH=200
scroll=0
bg_scroll=0
game_over=False
score=0
fade_counter = 0
high_score=0


# Define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
PANEL = (153,217,234)

# Load fonts
font_small = pygame.font.SysFont('Lucida Sans', 16)
font_big = pygame.font.SysFont('Lucida Sans', 24)


# Load Assets
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
player_image = pygame.image.load('assets/jump.png').convert_alpha()
platform_image = pygame.image.load('assets/wood.png').convert_alpha()


def draw_text(text, font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))


def draw_bg(bg_scroll):
        screen.blit(bg_image,(0,bg_scroll))
        screen.blit(bg_image,(0,-600 + bg_scroll))


def draw_pannel(score):
    pygame.draw.line(screen,WHITE,(0,25),(SCREEN_WIDTH,25))
    pygame.draw.rect(screen,PANEL,(0,0,SCREEN_WIDTH,25))
    draw_text("SCORE: "+str(score), font_small, WHITE,0,0)
    draw_text("HIGH SCORE: "+str(high_score),font_small,WHITE,250,0)

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
        scroll=0
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

        if(self.rect.top<=SCROLL_THRESH):
            if(self.vel_y < 0):
                scroll = -dy

        self.rect.x+=dx
        self.rect.y+=dy
        return scroll


    def draw(self):
        screen.blit( pygame.transform.flip(self.image,self.flip,False), (self.rect.x - 10,self.rect.y - 5))   
        pygame.draw.rect(screen,WHITE,self.rect,2)


class Platform(pygame.sprite.Sprite):
    def __init__(self,width,x,y, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width,10))
        self.rect = self.image.get_rect()
        self.moving = moving
        self.speed = random.randint(1,2)
        self.move_counter = random.randint(0,50)
        self.direction = random.choice([-1,1])
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):

        if(self.moving):
            self.move_counter+=1
            self.rect.x += self.direction * self.speed

        if self.move_counter > 100 or self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.direction *=-1
            self.move_counter=0


        self.rect.y +=scroll
        
        if(self.rect.top > SCREEN_HEIGHT):
            self.kill()


if(os.path.exists("score.txt")):
    with open("score.txt") as f:
        high_score = int(f.read())

# Player instance
jumpy = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)


# Platform
platform_group = pygame.sprite.Group()
platform = Platform(100, SCREEN_WIDTH//2 - 50,SCREEN_HEIGHT -90, False)
platform_group.add(platform)





run =True
while run:
    clock.tick(FPS)
    if(not game_over):
        scroll=jumpy.move()
        bg_scroll+=scroll

        if(bg_scroll>=600):
            bg_scroll=0
        draw_bg(bg_scroll)


        if(len(platform_group)<10):
            p_moving=False
            p_w = random.randint(40,60)
            p_x = random.randint(0,SCREEN_WIDTH-p_w)
            p_y = platform.rect.y - random.randint(80,120)
            p_type = random.randint(1,2)
            if p_type==1 and score>1000:
                p_moving=True
            platform = Platform(p_w,p_x,p_y,p_moving)
            platform_group.add(platform)


        if scroll > 0:
            score+=scroll


        if high_score < score:
            high_score=score



        platform_group.draw(screen)
        platform_group.update(scroll)
        jumpy.draw()
        draw_pannel(score)
        if(jumpy.rect.top>SCREEN_HEIGHT):
            game_over=True

    else:
        with open("score.txt", 'w') as f:
            f.write(str(high_score))
        if(fade_counter<SCREEN_HEIGHT):
            fade_counter+=5
            for y in range(0,6,2):
                pygame.draw.rect(screen, BLACK,(0,y*100,fade_counter,100))
                pygame.draw.rect(screen, BLACK,(SCREEN_WIDTH-fade_counter,(y+1)*100,SCREEN_WIDTH,100))
            
        else:
            draw_text("GAME OVER!", font_big,WHITE, 130, 200)
            draw_text("SCORE: "+str(score), font_big,WHITE, 130, 250)
            draw_text("PRESS SPACE TO PLAY AGAIN", font_big,WHITE, 40, 300)
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game_over = False
                scroll=0
                score=0
                fade_counter=0
                jumpy.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)
                platform_group.empty()
                platform = Platform(100, SCREEN_WIDTH//2 - 50,SCREEN_HEIGHT -90, False)
                platform_group.add(platform)


    # Event Handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            with open("score.txt", 'w') as f:
                f.write(str(high_score))
            run=False
    pygame.display.update()
pygame.quit()