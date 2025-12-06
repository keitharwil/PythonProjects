import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def out_of_bounds(self):
        if self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0

        if self.rect.top < 10:
            self.rect.top = 10

        if self.rect.bottom > WINDOW_HEIGHT - 10:
            self.rect.bottom = WINDOW_HEIGHT - 10

    
    def update(self, dt):
        key = pygame.key.get_pressed()    
        self.direction.y = (int(key[pygame.K_s]) - int(key[pygame.K_w])) or (int(key[pygame.K_DOWN]) - int(key[pygame.K_UP]))
        self.direction.x = (int(key[pygame.K_d]) - int(key[pygame.K_a])) or (int(key[pygame.K_RIGHT]) - int(key[pygame.K_LEFT]))
        
        self.rect.center += self.direction * self.speed * dt
        self.direction = self.direction.normalize() if self.direction else self.direction

        key_just_pressed = pygame.key.get_just_pressed()
        if key_just_pressed[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
        self.out_of_bounds()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT))) 

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.meteor_lifetime = 3000
        self.start_time = pygame.time.get_ticks()

    def update(self, dt):
        self.rect.centery += 400 * dt
        meteor_spawned_time = pygame.time.get_ticks()
        if meteor_spawned_time - self.start_time>= self.meteor_lifetime:
            self.kill()
        
# general setup
pygame.init()
pygame.display.set_caption("SPACE SHOOTER")
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

#import
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
for _ in range(20): Star(all_sprites, star_surf)
player = Player(all_sprites)
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH),randint(-200, -100)), all_sprites)
    all_sprites.update(dt)
    display_surface.fill("darkgray")
    all_sprites.draw(display_surface)

    pygame.display.update()
    
pygame.quit()