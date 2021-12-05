import pygame

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy")


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
    
    def draw(self):
        screen.blit(self.image, (self.rect.x - 10,self.rect.y - 5))   
        pygame.draw.rect(screen,WHITE,self.rect,2)

jumpy = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT - 150)

run =True
while run:
    screen.blit(bg_image,(0,0))


    jumpy.draw()

    # Event Handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()