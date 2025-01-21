import pygame, random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Groups")

FPS = 60
clock = pygame.time.Clock()

#define classes
class Player(pygame.sprite.Sprite):
    """class for player to fight monsters"""
    def __init__(self, x,y, monster_group) -> None:
        super().__init__()
        self.image = pygame.image.load("cursus-advansed/intermediate-pygame/Sprites/Sp/knight.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = 5
        self.monster_group = monster_group

    def move(self):
        """move player continoulsy"""
        #get pressed keys
        keys = pygame.key.get_pressed()
        #move dragon 
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] or keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

    def check_collisions(self):
        """check collisions for player and monster"""
        if pygame.sprite.spritecollide(self, self.monster_group, True):
            print(len(self.monster_group))

    def update(self):
        """update player"""
        self.move()
        self.check_collisions()



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

#create a monster group and make 10 monsters
my_monster_group = pygame.sprite.Group()
for i in range(10):
    monster = Monser(i*64, 10)
    my_monster_group.add(monster)

#creat player group
player_group = pygame.sprite.Group()
player = Player(500, 500, my_monster_group)
player_group.add(player)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill((0,0,0))

    #Update and Draw assets
    player_group.update()
    player_group.draw(display_surface)
    my_monster_group.update()
    my_monster_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
