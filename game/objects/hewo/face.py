import pygame
from game.objects.hewo.eye import Eye
from game.objects.hewo.mouth import Mouth
from game.settings import SettingsLoader

PHI = (1 + 5 ** (1 / 2)) / 2

class Face:
    def __init__(self, settings=None):
        self.settings = settings
        if self.settings is None:
            self.settings = SettingsLoader().load_settings("game.settings.hewo")  # Si no se pasa nada, usa la configuración de 'face' en settings
            print("using default settings")
        self.size = [PHI * self.settings['face']['size'],
                     self.settings['face']['size']]
        self.position = self.settings['face']['position']
        self.color = tuple(self.settings['face']['bg_color'])
        self.max_size = self.settings['face']['max_size']

        # Superficie de la cara
        self.face_surface = pygame.Surface(self.size)

        # Tamaños proporcionales de ojos y boca
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        # Posiciones de los elementos en la cara
        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        # Inicialización de los ojos y la boca usando settings correspondientes
        self.mouth_settings = self.settings['mouth']
        self.left_eye_settings = self.settings['eye']
        self.right_eye_settings = self.settings['eye']

        self.mouth = Mouth(self.mouth_size, self.mouth_pos, settings=self.mouth_settings)
        self.left_eye = Eye(self.eye_size, self.left_eye_pos, settings=self.left_eye_settings, object_name="Left Eye")
        self.right_eye = Eye(self.eye_size, self.right_eye_pos, settings=self.right_eye_settings, object_name="Right Eye")


    def update_face(self):
        self.face_surface = pygame.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]
        self.left_eye_pos = [0, 0]  # Posición en la superficie
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]
        # ACTUALIZAR
        self.left_eye.position = self.left_eye_pos
        self.right_eye.position = self.right_eye_pos
        self.mouth.position = self.mouth_pos
        self.left_eye.size = self.eye_size
        self.right_eye.size = self.eye_size
        self.mouth.size = self.mouth_size


    def set_size(self, size):
        self.size[0] = max(PHI, min(size[0], self.max_size[0]))
        self.size[1] = max(1, min(size[1], self.max_size[1]))

    def set_position(self, pos):
        self.position[0] = max(0, min(pos[0], self.max_size[0] - self.size[0]))
        self.position[1] = max(0, min(pos[1], self.max_size[1] - self.size[1]))

    def update(self):
        self.update_face()
        self.left_eye.update()
        self.right_eye.update()
        self.mouth.update()

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)

    def draw(self, surface):
        self.face_surface.fill(self.color)
        self.left_eye.draw(self.face_surface)
        self.right_eye.draw(self.face_surface)
        self.mouth.draw(self.face_surface)
        surface.blit(self.face_surface, dest=self.position)



# Test face object
def test_component():
    pygame.init()
    settings = SettingsLoader().load_settings("game.settings.hewo")
    print(settings)
    screen = pygame.display.set_mode((800, 600))
    face = Face()
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 255, 255))
        face.update()
        face.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            face.handle_event(event)


if __name__ == '__main__':
    test_component()