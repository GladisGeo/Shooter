import math
import pygame
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            pygame.Color('dodgerblue1'),
            ((0, 0), (50, 15), (0, 30)))
        self.rect = self.image.get_rect(center=pos)
        self.orig_img = self.image
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)

    def update(self):
        self.rotate()
        self.pos += self.vel
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def rotate(self):

        mouse_pos = pygame.mouse.get_pos()
        # Calculate the vector to the mouse position by subtracting
        # the self.pos vector from the mouse_pos.
        rel_x, rel_y = mouse_pos - self.pos
        # Use math.atan2 to get the angle in radians and convert it to degrees.
        angle = -math.degrees(math.atan2(rel_y, rel_x))
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_img, angle, 1)
        # Update the rect and keep the center at the old position.
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    player = Player((300, 200))
    sprite_group.add(player)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        sprite_group.update()
        screen.fill((30, 30, 30))
        sprite_group.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()