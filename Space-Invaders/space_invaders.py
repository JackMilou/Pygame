import pygame, random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")


FPS = 60
clock = pygame.time.Clock()

class Game():
    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.round_number = 3
        self.score = 0

        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        # self.max_bullet = Alien.max_alien_bullets

        self.new_round = pygame.mixer.Sound("Space-Invaders/Sound/new_round.wav")
        self.breach = pygame.mixer.Sound("Space-Invaders/Sound/breach.wav")
        self.alien_hit = pygame.mixer.Sound("Space-Invaders/Sound/alien_hit.wav")
        self.player_hit = pygame.mixer.Sound("Space-Invaders/Sound/player_hit.wav")

        self.new_round.set_volume(.2)
        self.breach.set_volume(.15)
        self.alien_hit.set_volume(.1)
        self.player_hit.set_volume(.1)

        self.font = pygame.font.Font("Space-Invaders/Other/Facon.ttf", 32)

    def update(self):
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        WHITE = (255,255,255)

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH//2
        score_rect.top = 10

        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20,10)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)


    def shift_aliens(self):
        #check if alien hit edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                shift = True

        #shift alien and revers and move alien off edge
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                alien.rect.y += 10

                alien.direction = -1*alien.direction
                alien.rect.x += alien.direction*alien.velocity

                if alien.rect.bottom >= WINDOW_HEIGHT - 100:
                    breach = True
            if breach:
                self.breach.play()
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line!", "Press 'Enter' to continue")

    def check_collisions(self):
        #player hit alien
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.alien_hit.play()
            self.score += 100
        #alien hit player
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player_hit.play()
            self.player.lives -= 1

            # self.check_game_status("You've been hit", "Press 'Enter' to continue")

            #check lives
            if self.player.lives <= 0:
                self.player.reset()
                self.reset_game()


    def check_round_completion(self):
        #check aliens left
        if not (self.alien_group):
            self.score += 200*self.round_number
            self.round_number += 1

            if self.player.lives < 5:
                self.player.lives += 1
            # self.max_bullet += 1

            self.start_new_round()


    def start_new_round(self):
        self.player_bullet_group.empty()
        for i in range(11):
            for j in range(5):
                alien = Alien(64 + i*64, 64 + j*64, self.round_number, self.alien_bullet_group)
                self.alien_group.add(alien)
        self.new_round.play()
        self.pause_game("Space Invaders round " + str(self.round_number), "Press 'Enter' to continue")

    def check_game_status(self, main_text, sub_text):
        #Empty all bullets and reset player and aliens
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()
        
        #check gameover
        if self.player.lives <= 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        global running

        WHITE = (255,255,255)
        BLACK = (0,0,0)

        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
        

    def reset_game(self):
        self.pause_game("Final score: " + str(self.score) + "    Final round: " + str(self.round_number),"Press 'Enter' to play again")

        self.score = 0
        self.round_number = 1

        self.player.lives = 5

        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()

        self.start_new_round()

class Player(pygame.sprite.Sprite):

    def __init__(self, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Space-Invaders/Images/hamburger.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("Space-Invaders/Sound/player_fire.wav")
        self.shoot_sound.set_volume(.1)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

        self.max_player_bullets = 4

    def fire(self):
        if len(self.bullet_group) < self.max_player_bullets:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH//2

class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Space-Invaders/Images/kipnugget.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.direction = 1
        
        if velocity > 4:
            self.velocity = velocity
            # self.velocity = 4
        else:
            self.velocity = velocity

        self.bullet_group = bullet_group
        self.max_alien_bullets = 3

        self.frame_count = 0
        self.alien_fire_timer = 0        

        self.shoot_sound = pygame.mixer.Sound("Space-Invaders/Sound/alien_fire.wav")
        self.shoot_sound.set_volume(.05)

    def update(self):
        self.rect.x += self.direction*self.velocity

        self.frame_count += 1
        if self.frame_count == FPS:
            self.alien_fire_timer += 1
            self.frame_count = 0

        if self.alien_fire_timer >= 2:
            if random.randint(0, 1000) > 999 and len(self.bullet_group) < self.max_alien_bullets:
                self.shoot_sound.play()
                self.fire()

    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_goup):
        super().__init__()
        self.image = pygame.image.load("Space-Invaders/Images/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_goup.add(self)

    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Space-Invaders/Images/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        self.rect.y += self.velocity

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
    
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

my_alien_group = pygame.sprite.Group()

#test alien
# for i in range(10):
#     alien = Alien(64 + i*64, 100, 3, my_alien_bullet_group)
#     my_alien_group.add(alien)

my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.start_new_round()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()

    display_surface.fill((0,0,0))

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()

    #tick the clock
    clock.tick(FPS)

pygame.quit()