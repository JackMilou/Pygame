import pygame, random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Collide")

FPS = 60
clock = pygame.time.Clock()

#classes
class Game():
    """help manage our game"""
    def __init__(self):
        pass

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        pass


class Knight(pygame.sprite.Sprite):
    """class to represent a knight"""
    def __init__(self, x, y) -> None:
        super().__init__()
        # self.image = pygame.image.load("Sp/blue_monster.png")
        self.image = pygame.image.load("cursus-advansed/intermediate-pygame/Sprites/Sp/knight.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = random.randint(1,5)

    def update(self):
        """update and move monster"""
        self.rect.y -= self.velocity

class Monser(pygame.sprite.Sprite):
    """class to represent a monster"""
    def __init__(self, x, y) -> None:
        super().__init__()
        # self.image = pygame.image.load("Sp/blue_monster.png")
        self.image = pygame.image.load("cursus-advansed/intermediate-pygame/Sprites/Sp/blue_monster.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = random.randint(1,5)

    def update(self):
        """update and move monster"""
        self.rect.y += self.velocity

#create group
my_monster_group = pygame.sprite.Group()
for i in range(12):
    monster = Monser(i*64, 10)
    my_monster_group.add(monster)

my_knight_group = pygame.sprite.Group()
for i in range(12):
    knight = Knight(i*64, WINDOW_HEIGHT - 64)
    my_knight_group.add(knight)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()