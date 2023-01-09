from typing import List

import pygame
from pygame import Color
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_RETURN


class ScreenInterface:
    def handle_events(self, events: List[pygame.event.Event]): ...
    def update(self): ...
    def draw(self, surface: pygame.surface.Surface): ...


class MyScreen:
    def __init__(self):
        # track
        self.track = pygame.image.load("24.PNG").convert()

        # pygame surface screen
        self.x = -980
        self.y = -1100

        # track surface
        self.surface_x = 1450
        self.surface_y = 1450

        # player / human
        self.human_x = 470
        self.human_y = 350
        self.human_xy = (self.human_x, self.human_y)

        self.human_w_or_h = 50

        self.human = pygame.image.load("IMG_3124.PNG").convert()
        self.humanrightsize = pygame.transform.scale(self.human, (self.human_w_or_h, self.human_w_or_h))

        self.step = 10
        self.direction = [0, 0]

        #  monster
        self.monster_w_or_h = 150

        self.monster = pygame.image.load("IMG_3125.PNG").convert()
        self.monsterrightsize = pygame.transform.scale(self.monster, (self.monster_w_or_h, self.monster_w_or_h))

        self.monstersurface = pygame.Surface.copy(self.track)

        self.monstercorrdinate = []

        self.scare_x = 500
        self.scare_y = 500

        self.timeappear = 30

        # colour
        self.BLACK = (0, 0, 0)

        # game stat
        self.counter = 0
        self.die = 0


    
    def handle_events(self, events: List[pygame.event.Event]): 
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.game_start = True


    def update(self, surface: pygame.surface.Surface): 
        self.monster_x = self.surface_x + self.scare_x - 60
        self.monster_y = self.surface_y + self.scare_y 
        self.surface_human_xy = [self.surface_x, self.surface_y]

        #getting the subsurface OF THE HUMAN to determine if there is colour
        subsurface_player = self.track.subsurface ((self.surface_x, self.surface_y, self.human_w_or_h, self.human_w_or_h))
        cliprect_player = subsurface_player.get_bounding_rect(255)
        # self.rect_player = subsurface_player.get_offset

        self.counter += 1

        self.scare_x = 500
        self.scare_y = 500

        # direction control
        if cliprect_player == (0, 0, 0, 0):
            #     # if the subsurface is empty (aka not of the track)
            #     # then go to the opposite direction
            self.direction[0] *= -1
            self.direction[1] *= -1
        else:
            #if keys are being press, give direction corrdinate [x, y]
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction = [0, 1]
            elif keys[pygame.K_DOWN]:
                self.direction = [0, -1]
            elif keys[pygame.K_LEFT]:
                self.direction = [-1, 0]
            elif keys[pygame.K_RIGHT]:
                self.direction = [1, 0]
            else:
                self.direction = [0, 0]

        
        # after obtaining the direction determine 
        # 1) self.x (the track moving)
        # 2) self.surface_x (the subsurface moving)
        # 3) self.scare_x (the x direction of the monster appearing)
        # 4) self.scare_y (the y direction of the monster appearing)
        if self.direction == [0, 0]:
            pass
        elif self.direction[0] == 0:
            self.y += (self.step * self.direction[1])
            self.surface_y -= (self.step * self.direction[1])
            self.scare_y *= -self.direction[1]
            self.scare_x = 0
        elif self.direction[1] == 0:
            self.x -= (self.step * self.direction[0])
            self.surface_x += (self.step * self.direction[0])
            self.scare_x *= self.direction[0]
            self.scare_y = 0

        # 
        if self.counter % self.timeappear == 0:
            if 0 <= self.monster_x <= 3000 and  0 <= self.monster_y < 2780:
                self.monstercorrdinate.append([self.monster_x, self.monster_y])  

                
        for i, n in enumerate (self.monstercorrdinate):
            subsurface_monster = self.track.subsurface ((n[0], n[1], self.human_w_or_h, self.human_w_or_h))
            self.cliprect_monster = subsurface_monster.get_bounding_rect(255)
            # self.rect_monster = subsurface_monster.get_offset

            if self.cliprect_monster == (0, 0, 0, 0):
                del self.monstercorrdinate[i]

        if len(self.monstercorrdinate) > 2:
            del self.monstercorrdinate[0]
        
        self.checking()

    def checking(self):
        for n in self.monstercorrdinate:
            if n[0] - self.human_w_or_h <= self.surface_human_xy[0] <= n[0] + self.monster_w_or_h:
                if n[1]- self.human_w_or_h <= self.surface_human_xy[1] <= n[1] + self.monster_w_or_h:
                    self.die += 1

        print(self.monstercorrdinate)
        print(self.surface_human_xy)
        print(self.die)


    def draw(self, surface: pygame.surface.Surface):
        surface.fill(self.BLACK)  # always the first drawing command

        self.monstersurface = pygame.Surface.copy(self.track)

        for n in self.monstercorrdinate:
            self.monstersurface.blit(self.monsterrightsize, (n[0], n[1]))

        surface.blit(self.monstersurface, (self.x, self.y))

        surface.blit(self.humanrightsize, (self.human_xy))



class Game:
    instance: 'Game'

    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.SIZE = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()

        self.current_screen = MyScreen()

        Game.instance = self
    

    # @classmethod
    # def set_screen(cls, new_screen: ScreenInterface):
    #     cls.instance.current_screen = new_screen

    
    def run(self):
        running = True
        while running:
            # EVENT HANDLING
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                    

            self.current_screen.handle_events(events)
            self.current_screen.update(self.screen)
            self.current_screen.draw(self.screen)

            # Must be the last two lines
            # of the game loop
            pygame.display.flip()
            self.clock.tick(30)
            #---------------------------


        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
