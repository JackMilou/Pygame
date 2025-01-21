import pygame, random

vector = pygame.math.Vector2

pygame.init()

#1280/32 = 40   736/32 = 23
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("KILL THEM ALL")

FPS = 60
clock = pygame.time.Clock()

#def classes
class Game():
    def __init__(self, player, enemy_group, platform_group, portal_group, bullet_group, ruby_group):
        super().__init__()

        self.STARTING_ROUND_TIME = 30
        self.STARTING_ENEMY_CREATION_TIME = 5
        
        self.score = 0
        self.round_num = 1
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME 
        self.enemy_creation_time = self.STARTING_ENEMY_CREATION_TIME
        self.max_enemy_speed = self.round_num + 2
        self.min_enemy_speed = 1
        self.max_enemy_speed_limit = 12
        self.creation_decrease = 0.5

        self.title_fond = pygame.font.Font("fonts/Poultrygeist.ttf", 48)
        self.title_fond_small = pygame.font.Font("fonts/Poultrygeist.ttf", 30)
        self.HUD_fond = pygame.font.Font("fonts/pixel.ttf", 24)

        #sounds
        self.lost_ruby_sound = pygame.mixer.Sound("sounds/lost_ruby.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("sounds/ruby_pickup.wav")
        pygame.mixer.music.load("sounds/level_music.wav")

        self.lost_ruby_sound.set_volume(.1)
        self.ruby_pickup_sound.set_volume(.1)
        pygame.mixer.music.set_volume(.1)

        #groups and sprites
        self.player = player
        self.enemy_group = enemy_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group

    def update(self):
        #update round time
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0

        self.check_collisions()
        self.add_enemy()
        self.check_round_completion()
        self.check_game_over()

    def draw(self):
        #colors
        WHITE = (255,255,255)
        GREEN = (25,200,25)

        #text
        score_text = self.HUD_fond.render("Score: "+ str(self.score),True,WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 50)

        health_text = self.HUD_fond.render("Health: "+ str(self.player.health),True,WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 25)

        title_text = self.title_fond.render("Kill Them all",True,GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 25)

        round_text = self.HUD_fond.render("Night: "+ str(self.round_num),True,WHITE)
        round_rect = round_text.get_rect()
        round_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 50)

        time_text = self.HUD_fond.render("Sunrise In: "+ str(self.round_time),True,WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 25)

        #draw hud
        display_surface.blit(score_text,score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text,title_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(time_text,time_rect)


    def add_enemy(self):
        #check to add a enemy every second 
        if self.frame_count % FPS == 0:
            #olny add enemy if creation time has passed
            if self.round_time % self.enemy_creation_time == 0:
                if self.max_enemy_speed < self.max_enemy_speed_limit:
                    self.max_enemy_speed = self.round_num + 3
                    if self.round_num > 3:
                        self.min_enemy_speed = self.round_num - 2
                else:
                    self.max_enemy_speed = self.max_enemy_speed_limit
                    self.min_enemy_speed = self.max_enemy_speed_limit - 3
            
                enemy = Enemy(self.platform_group, self.portal_group, self.min_enemy_speed, self.max_enemy_speed)
                self.enemy_group.add(enemy)

    def check_collisions(self):
        #check if bullet hit enemy
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, False)
        if collision_dict:
            for enemys in collision_dict.values():
                for enemy in enemys:
                    enemy.hit_sound.play()
                    enemy.is_dead = True
                    enemy.animate_death = True
        
        #check enemy collision with player
        collision_list = pygame.sprite.spritecollide(self.player, self.enemy_group, False)
        if collision_list:
            for enemy in collision_list:
                #check enemy is dead
                if enemy.is_dead == True:
                    enemy.kick_sound.play()
                    enemy.kill()
                    self.score += 25

                    ruby = Ruby(self.platform_group, self.portal_group)
                    self.ruby_group.add(ruby)
                else:
                    self.player.health -= 20
                    self.player.hit_sound.play()
                    #move player to stop more hits
                    # self.player.position.x -= 56*enemy.direction
                    # self.player.rect.bottomleft = self.player.position
                    self.player.position.x = WINDOW_WIDTH - 50
                    self.player.position.y = 220
                    self.player.left_save_zone = False

        #player collided with ruby
        if pygame.sprite.spritecollide(self.player, self.ruby_group, True):
            self.ruby_pickup_sound.play()
            self.score += 100
            self.player.health += 10
            if self.player.health > self.player.STARTING_HEALTH:
                self.player.health = self.player.STARTING_HEALTH
        
        #check living enemy collide with ruby
        for enemy in self.enemy_group:
            if enemy.is_dead == False:
                if pygame.sprite.spritecollide(enemy, self.ruby_group, True):
                    self.lost_ruby_sound.play()
                    enemy = Enemy(self.platform_group, self.portal_group, self.min_enemy_speed, self.max_enemy_speed)
                    self.enemy_group.add(enemy)
                    

    def check_round_completion(self):
        if self.round_time == 0:
            self.start_new_round()

    def check_game_over(self):
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game("YOU DIED... score: " + str(self.score), "Press 'ENTER' to play again")
            self.reset()

    def start_new_round(self):
        self.round_num += 1 
        if self.round_num < self.enemy_creation_time:
            self.enemy_creation_time -= self.creation_decrease

        #reset values
        self.round_time = self.STARTING_ROUND_TIME

        self.enemy_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()

        self.player.reset()

        self.pause_game("YOU SURVIVED..", "Press 'ENTER' to continue")


    def pause_game(self, main_text, sub_text):
        global running

        pygame.mixer.music.pause()

        #set collors
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        GREEN = (25,200,25)

        #text
        main_text = self.title_fond.render(main_text, True, GREEN)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        sub_text = self.title_fond_small.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

        #display the pause game
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #pause game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #user wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.unpause()
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()


    def reset(self):
        self.score = 0
        self.round_num = 1
        self.round_time = self.STARTING_ROUND_TIME
        self.enemy_creation_time = self.STARTING_ENEMY_CREATION_TIME

        #player
        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()

        #sprites
        self.enemy_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()

        #music
        pygame.mixer.music.play(-1,0.0)



class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        super().__init__()
        #load img
        #dirt
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (1).png"), (32,32))
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (2).png"), (32,32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (3).png"), (32,32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (4).png"), (32,32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (5).png"), (32,32))
            sub_group.add(self)
        elif image_int == 10:
            self.image = pygame.transform.scale(pygame.image.load("images/tilesave/Tile (10).png"),(32,32))
            sub_group.add(self)
        elif image_int == 11:
            self.image = pygame.transform.scale(pygame.image.load("images/tilesave/Tile (11).png"),(32,32))
            self.image.set_alpha(128)
            sub_group.add(self)
        
        
        main_group.add(self)

        #get rect end pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        #create mask
        self.mask = pygame.mask.from_surface(self.image)
        

class Player(pygame.sprite.Sprite):


    def __init__(self, x, y, platform_group, portal_group, bullet_group, wall_group, save_group):
        super().__init__()

        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.8 #gravity
        self.VERTICAL_JUMP_SPEED = 18
        self.STARTING_HEALTH = 100

        #animation frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        #move
        for i in range(9):
                self.move_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/run/Run__00{i}.png"), (64,64)))

        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #idle
        for i in range(9):
                self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/idle/Idle__00{i}.png"), (32,64)))

        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #jump
        for i in range(9):
                self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/jump/Jump__00{i}.png"), (64,64)))
        
        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #attack
        for i in range(9):
                self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/player/attack/Attack__00{i}.png"), (64,64)))
        
        for sprite in self.attack_right_sprites:
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #attach sprite group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.wall_group = wall_group
        self.save_group = save_group

        #Animation booleans
        self.animate_jump = False
        self.animate_fire = False

        #sounds
        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
        
        self.jump_sound.set_volume(.1)
        self.slash_sound.set_volume(.1)
        self.portal_sound.set_volume(.1)
        self.hit_sound.set_volume(.1)

        #kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        #set intial player values
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y

        self.current_time = 0

        self.left_save_zone = False
        self.in_save_zone = False
        self.save_zone_min_time = 1000
        self.save_zone_max_time = 1500
        self.save_zone_entery_time = 0
        self.lever = False
        


    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.move()
        self.check_collisions()
        self.check_animations()

        #update mask and create mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        #set acceleration vactor
        if self.in_save_zone == False:
            self.acceleration = vector(0, self.VERTICAL_ACCELERATION)
        else:
            self.acceleration = vector(0,0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .2)
        elif keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .2)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .2)
            else:
                self.animate(self.idle_left_sprites, .2)

        #calculate new kinematics values
        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #update rect and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 5
                self.velocity.y = 0
        #collision check jumping up
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position
        #collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position
        #collision for save
        collided_save = pygame.sprite.spritecollide(self, self.save_group, False)
        if collided_save:
            if self.left_save_zone == False:
                # print("Player in the save zone")
                self.in_save_zone = True #turns off gravity
                self.position.y = 200
                self.lever = True

                if self.save_zone_entery_time == 0:
                    self.save_zone_entery_time = self.current_time
            # else:
            #     if self.velocity.x > 0:  #entering from right side
            #         self.position.x = collided_save[0].rect.left - self.rect.width
            #     elif self.velocity.y < 0:
            #         self.position.y = collided_save[0].rect.bottom - self.rect.height
        else:
            if self.current_time - self.save_zone_entery_time >= self.save_zone_min_time: 
                #makes it so the player can't instantly get out of the save zone 
                self.left_save_zone = True
                self.save_zone_entery_time = 0
                self.in_save_zone = False 
                self.lever = False
                
            else:
                if self.lever: #so you dont start in de save zone
                    self.position.y = 220
                    self.position.x = WINDOW_WIDTH - 50
                    

    def check_animations(self):

        #animate jump
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, .01)
            else:
                self.animate(self.jump_left_sprites, .01)
        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, .01)
            else:
                self.animate(self.attack_left_sprites, .01)

    def jump(self):
        #only jump on platform
        if pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask):
            self.jump_sound.play()
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def fire(self):
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True

    def reset(self):
        self.velocity = vector(0,0)
        self.position = vector(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            #End jump animation
            if self.animate_jump:
                self.animate_jump = False
            #End attack animation
            if self.animate_fire:
                self.animate_fire = False

        self.image = sprite_list[int(self.current_sprite)]
        
 
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group, player):
        super().__init__()
        
        self.VELOCITY = 20
        self.RANGE = 500

        #load img end get rect
        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"),(64,64))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/player/slash.png"),True,False),(64,64))
            self.VELOCITY = -1*self.VELOCITY

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.starting_x = x

        bullet_group.add(self)


    def update(self):
        self.rect.x += self.VELOCITY

        #if bullet passed range kill it
        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        super().__init__()
        
        self.VERTICAL_ACCELERATION = 3 #gravity
        self.RISE_TIME = 2
        
        #animation 
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        enemy_type = random.randint(0,1)
        if enemy_type == 0:
            #walk
            for i in range(1, 11, 1):
                self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/dog/walk/Walk ({i}).png"), (64,64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))
            
            #die
            for i in range(1, 11, 1):
                self.die_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/dog/dead/Dead ({i}).png"), (64,64)))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #rise
            for i in range(10, 0, -1):
                self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/dog/dead/Dead ({i}).png"), (64,64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        elif enemy_type == 1:
            #walk
            for i in range(1, 11, 1):
                self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/cat/walk/Walk ({i}).png"), (64,64)))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))
            
            #die
            for i in range(1, 11, 1):
                self.die_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/cat/dead/Dead ({i}).png"), (64,64)))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #rise
            for i in range(10, 0, -1):
                self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load(f"images/enemy/cat/dead/Dead ({i}).png"), (64,64)))

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #load img and get rect
        self.direction = random.choice([-1,1])

        self.current_sprite = 0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.current_sprite]
        else:
            self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH - 100), -100)

        #attach sprite group
        self.platform_group = platform_group
        self.portal_group = portal_group

        #animation booleans
        self.animate_death = False
        self.animate_rise = False

        #sounds
        self.hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav")
        self.kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")

        self.hit_sound.set_volume(.1)
        self.kick_sound.set_volume(.1)
        self.portal_sound.set_volume(.1)

        #vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction*random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        #initial values 
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0

        print(self.velocity)

    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()

        #determine when the enemy should rise from the dead
        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True
                    #when enemy died current sprite ended on the last animation frame 
                    #we want to start at 0
                    self.current_sprite = 0 

    def move(self):
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, .2)
            else:
                self.animate(self.walk_right_sprites, .2)
            
            #calculate new kinematics values
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5*self.acceleration

            #update rect and add wrap around movement
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0

            self.rect.bottomleft = self.position

    def check_collisions(self):
        
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        #collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        #animate enemy death
        if self.animate_death:
            if self.direction == -1:
                self.animate(self.die_left_sprites, .03)
            else:
                self.animate(self.die_right_sprites, .03)
        #animate enemy rise
        if self.animate_rise:
            if self.direction == -1:
                self.animate(self.rise_left_sprites, .04)
            else:
                self.animate(self.rise_right_sprites, .04)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            #end animations
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False
            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
                self.frame_count = 0
                self.round_time = 0

        self.image = sprite_list[int(self.current_sprite)]
    

class RubyMaker(pygame.sprite.Sprite):

    def __init__(self, x, y, main_group):
        super().__init__()

        #animation frames
        self.ruby_sprites = []

        #rotating
        for i in range(6):
            self.ruby_sprites.append(pygame.transform.scale(pygame.image.load(f"images/ruby/tile00{i}.png"), (64,64)))
            # self.ruby_sprites.append(pygame.transform.scale(pygame.image.load(f"images/ruby/star-coin{i}.png"), (64,64)))
        
        #load img and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        #add to main group to draw
        main_group.add(self)

    def update(self):
        self.animate(self.ruby_sprites, 0.15)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Ruby(pygame.sprite.Sprite):
    
    def __init__(self, platform_group, portal_group):
        super().__init__()

        self.VERTICAL_ACCELERATION = 3 #Gravity
        self.HORIZONTAL_VELOCITY = 5

        #animation 
        self.ruby_sprites = []

        #rotating
        for i in range(6):
            self.ruby_sprites.append(pygame.transform.scale(pygame.image.load(f"images/ruby/tile00{i}.png"), (32,32)))

        #load img and get rect 
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WINDOW_WIDTH//2, 100)

        #sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        #sounds
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.portal_sound.set_volume(.1)

        #vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(random.choice([-1*self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)


    def update(self):
        self.animate(self.ruby_sprites, .1)
        self.move()
        self.check_collisions()

    def move(self):
        #calculate new kinematics values
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #update rect and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        #collision for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position


    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Portal(pygame.sprite.Sprite):

    def __init__(self, x, y, color, portal_group):
        super().__init__()

        #animation frames
        self.portal_sprites = []

        #portal animation
        if color == "green":
            for i in range(21):
                self.portal_sprites.append(pygame.transform.scale(pygame.image.load(f"images/portals/green/tile ({i}).png"), (72,72)))
        elif color == "purple":
            for i in range(21):
                self.portal_sprites.append(pygame.transform.scale(pygame.image.load(f"images/portals/purple/tile ({i}).png"), (72,72)))

        self.current_sprite = random.randint(0, len(self.portal_sprites) -1)
        self.image = self.portal_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        #add to potal group
        portal_group.add(self)

    def update(self):
        self.animate(self.portal_sprites, 0.07)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]

#create sprite groups
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
my_bullet_group = pygame.sprite.Group()

my_enemy_group = pygame.sprite.Group()

my_portal_group = pygame.sprite.Group()
my_ruby_group = pygame.sprite.Group()

my_wall_group = pygame.sprite.Group()
my_save_block_group = pygame.sprite.Group()

#create tile map 23 rows and 40 collums
#0 = no tile 1 = dirt 2-5 = platform 6 = ruby 7-8 = portals 9 = player
tile_map = [
    #1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0], #3
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11,10], #5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11,10], #6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10
    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4], #11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #15
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #16
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #17
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #18
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], #21
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], #22
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #23
]

for i in range(len(tile_map)):
    for j in range(len(tile_map[i])):
        #dirt
        if tile_map[i][j] == 1:
            Tile(j*32, i*32, 1, my_main_tile_group)
        #platforms
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 4:
            Tile(j*32, i*32, 4, my_main_tile_group, my_platform_group)
        elif tile_map[i][j] == 5:
            Tile(j*32, i*32, 5, my_main_tile_group, my_platform_group)
        #Ruby
        elif tile_map[i][j] == 6:
            RubyMaker(j*32, i*32, my_main_tile_group)
        elif tile_map[i][j] == 7:
            Portal(j*32, i*32, "green", my_portal_group)
        elif tile_map[i][j] == 8:
            Portal(j*32, i*32, "purple", my_portal_group)
        #player
        elif tile_map[i][j] == 9:
            my_player = Player(j*32 - 32, i*32 +32, my_platform_group, my_portal_group, my_bullet_group, my_wall_group, my_save_block_group)
            my_player_group.add(my_player)
        elif tile_map[i][j] == 10:
            Tile(j*32, i*32, 10, my_main_tile_group, my_wall_group)
        elif tile_map[i][j] == 11:
            Tile(j*32, i*32, 11, my_main_tile_group, my_save_block_group)
        

background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (1280, 736))
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

#create game
my_game = Game(my_player, my_enemy_group, my_platform_group, my_portal_group, my_bullet_group, my_ruby_group)
my_game.pause_game("-.- .. .-.. .-.-.- .-.-.-", "Press 'ENTER' to begin")
pygame.mixer.music.play(-1,0.0)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.jump()
            #player wants to fire 
            if event.key == pygame.K_w:
                my_player.fire()
            #rain enemy
            if event.key == pygame.K_RETURN:
                enemy = Enemy(my_platform_group, my_portal_group, 1, 3)
                my_enemy_group.add(enemy)

    display_surface.blit(background_image,background_rect)
    
    #draw tiles and update
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    #update and draw sprite group
    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_bullet_group.update()
    my_bullet_group.draw(display_surface)

    my_enemy_group.update()
    my_enemy_group.draw(display_surface)

    my_ruby_group.update()
    my_ruby_group.draw(display_surface)

    #update and draw game
    my_game.update()
    my_game.draw()
        
    pygame.display.update()
        
    clock.tick(FPS)

pygame.quit()