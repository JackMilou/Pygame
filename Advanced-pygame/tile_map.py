import pygame

#2d vectors
vector = pygame.math.Vector2

pygame.init()

# tile size = 32 so 960/32 = 30 tiles wide 640/32 = 20 tiles high
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tile map")

FPS = 60
clock = pygame.time.Clock()

#define classes
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        #load correct img and add to correct sub group
        if image_int == 1:
            self.image = pygame.image.load("Advanced-pygame/Image/dirt.png")
        elif image_int == 2:
            self.image = pygame.image.load("Advanced-pygame/Image/grass.png")
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.image.load("Advanced-pygame/Image/water.png")
            sub_group.add(self)
        #add all to main
        main_group.add(self)

        #get rect and posission
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def update(self):
        pygame.draw.rect(display_surface, (0,0,255), self.rect, 1)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()

        #animation frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        # self.dead_right_sprites = []
        # self.dead_left_sprites = []
        # self.jump_right_sprites = []
        # self.jump_left_sprites = []
        # self.max_run_sprites = 20

        #move right
        # if i < self.max_run_sprites:
        #     self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run ("+ str(i) +").png"),(64,64)))
        #     i +1
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (1).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (2).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (3).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (4).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (5).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (6).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (7).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (8).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (9).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (10).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (11).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (12).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (13).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (14).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (15).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (16).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (17).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (18).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (19).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Run (20).png"),(64,64)))

        #left
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #idle right
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (1).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (2).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (3).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (5).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (7).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (9).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (10).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (11).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (13).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (15).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("Advanced-pygame/Girl/Idle (16).png"),(64,64)))

        #left
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.current_sprite = 0
        self.image = self.move_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        self.starting_x = x
        self.starting_y = y

        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        self.posision = vector(x,y)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)

        self.HORIZONTAL_ACCELERATION = 1
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5 #Gravity
        self.VERTICAL_JUMP_SPEED = 15 #Determents how high we can jump

    def update(self):
        # pygame.draw.rect(display_surface, (255,255,0), self.rect, 1)
        self.mask = pygame.mask.from_surface(self.image)
        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image, (0,0,255), True, mask_outline)

        self.move()
        self.check_collisions()

    def move(self):
        self.acceleration = vector(0,self.VERTICAL_ACCELERATION)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .2)
            else:
                self.animate(self.idle_left_sprites, .2)

        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.posision += self.velocity + 0.5*self.acceleration

        #update rect and add wrap around motion
        if self.posision.x < 0:
            self.posision.x = WINDOW_WIDTH
        elif self.posision.x > WINDOW_WIDTH:
            self.posision.x = 0
        
        self.rect.bottomleft = self.posision


    def check_collisions(self):
        #check collisions
        collided_grass = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        collided_water = pygame.sprite.spritecollide(self, self.water_tiles, False)
        if collided_grass or collided_water and collided_grass:
            #only move to platform if player moves down
            if self.velocity.y > 0:
                self.posision.y = collided_grass[0].rect.top + 1
                self.velocity.y = 0
        elif collided_water:
            print("YOU CANT SWIM!!!!")
            self.posision = vector(self.starting_x, self.starting_y)
            self.velocity = vector(0,0)


    def jump(self):
        #only jump if on grass
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED

    def animate(self, sprite_list, speed):
        #loop sprite list change current sprite
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed 
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]


#create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()

#create tile map (20 rows 30 columns) (0 = no tile 1 = dirt 2 = grass 3 = water 4 = player)
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
]

#create tile objects from tile map
for i in range(len(tile_map)):
    # i moves us down j moves us accross
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            my_player = Player(j*32, i*32 + 32, grass_tile_group, water_tile_group)
            my_player_group.add(my_player)

background_image = pygame.image.load("Advanced-pygame/Image/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()

    display_surface.blit(background_image,background_rect)

    main_tile_group.draw(display_surface)
    main_tile_group.update()

    my_player_group.update()
    my_player_group.draw(display_surface)

    pygame.display.update()

    #tick the clock
    clock.tick(FPS)

pygame.quit()