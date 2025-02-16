import pygame
from settings import *

from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # getting animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # setting the player
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement setup
        self.direction = pygame.math.Vector2((0, 0))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 150

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool)
        }

        # tools
        self.selected_tool = 'axe'

    def use_tool(self):
        print(self.selected_tool)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': [],}

        for anim in self.animations.keys():
            full_path = 'assets/graphics/character/' + anim

            # getting the proper image
            self.animations[anim] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

        if keys[pygame.K_SPACE]:
            # timer for the tool use
            self.timers['tool use'].activate()
            self.direction = pygame.math.Vector2(0, 0)
            self.frame_index = 0

    def get_status(self):
        # checks if player is moving
        if self.direction.magnitude() == 0:
            # changing the animation status with split, so it doesn't add _idle
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def move(self, dt):

        # normalazing the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
