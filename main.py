import pygame
pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h 

screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("Escape Room")

running = True

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self):
        pass

player = Player(50, 50, 50, 50)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    player.draw()
    pygame.display.update()


pygame.quit()