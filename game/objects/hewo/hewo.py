import pygame
from game.objects.hewo.face import Face
from game.settings import SettingsLoader



class HeWo:
    def __init__(self, settings=None):
        self.settings = settings
        if self.settings is None:
            self.settings = SettingsLoader().load_settings("game.settings.hewo")
        self.face = Face(settings=self.settings)

    def draw(self, surface):
        self.face.draw(surface)

    def update(self):
        self.face.update()

    def handle_event(self, event):
        self.face.handle_event(event)


def test_component():
    pygame.init()
    settings = SettingsLoader().load_settings("game.settings.hewo")
    hewo = HeWo(settings=settings)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("HeWo Class")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            hewo.handle_event(event)

        hewo.update()
        hewo.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    test_component()