import random
import pygame
from game.objects.hewo.face import Face
from game.settings import SettingsLoader, create_logger


class HeWo(Face):
    def __init__(self, settings, object_name="HeWo"):
        self.logger = create_logger(object_name)
        self.settings = settings
        super().__init__(settings=self.settings)
        self.key_down_event = {
            pygame.K_SPACE: self.space_action,
            pygame.K_ESCAPE: self.escape_action,
            # pygame.K_a: self.increase_size,
            # pygame.K_b: self.decrease_size,
        }
        self.key_pressed_events = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right,
            pygame.K_a: self.increase_size,
            pygame.K_b: self.decrease_size,
        }
        self.step = 25

    def update(self):
        self.update_face()
        self.handle_keypressed()

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)

    def generate_random_vector(self, n=22):
        vec = [random.randint(0, 100) for _ in range(n)]
        self.logger.info("Generating random emotion vector")
        return vec

    def emotion_dict_from_values(self, values):
        return {
            'letl_a': values[0], 'letl_b': values[1], 'letl_c': values[2],
            'lebl_a': values[3], 'lebl_b': values[4], 'lebl_c': values[5],
            'retl_a': values[6], 'retl_b': values[7], 'retl_c': values[8],
            'rebl_a': values[9], 'rebl_b': values[10], 'rebl_c': values[11],
            'tl_a': values[12], 'tl_b': values[13], 'tl_c': values[14], 'tl_d': values[15], 'tl_e': values[16],
            'bl_a': values[17], 'bl_b': values[18], 'bl_c': values[19], 'bl_d': values[20], 'bl_e': values[21]
        }

    def get_emotion(self):
        letl, lebl = self.left_eye.get_emotion()
        retl, rebl = self.right_eye.get_emotion()
        tl, bl = self.mouth.get_emotion()
        emotion_dict = {
            'letl_a': letl[0], 'letl_b': letl[1], 'letl_c': letl[2],
            'lebl_a': lebl[0], 'lebl_b': lebl[1], 'lebl_c': lebl[2],
            'retl_a': retl[0], 'retl_b': retl[1], 'retl_c': retl[2],
            'rebl_a': rebl[0], 'rebl_b': rebl[1], 'rebl_c': rebl[2],
            'tl_a': tl[0], 'tl_b': tl[1], 'tl_c': tl[2], 'tl_d': tl[3], 'tl_e': tl[4],
            'bl_a': bl[0], 'bl_b': bl[1], 'bl_c': bl[2], 'bl_d': bl[3], 'bl_e': bl[4]
        }
        self.logger.info(f"Emotion Vector: {emotion_dict.values()}")
        self.logger.debug(f"Emotion Vector: {emotion_dict.values()}")
        return emotion_dict

    def set_emotion(self, emotion_dict):
        letl = [emotion_dict['letl_a'], emotion_dict['letl_b'], emotion_dict['letl_c']]
        lebl = [emotion_dict['lebl_a'], emotion_dict['lebl_b'], emotion_dict['lebl_c']]
        retl = [emotion_dict['retl_a'], emotion_dict['retl_b'], emotion_dict['retl_c']]
        rebl = [emotion_dict['rebl_a'], emotion_dict['rebl_b'], emotion_dict['rebl_c']]
        tl = [emotion_dict['tl_a'], emotion_dict['tl_b'], emotion_dict['tl_c'], emotion_dict['tl_d'],
              emotion_dict['tl_e']]
        bl = [emotion_dict['bl_a'], emotion_dict['bl_b'], emotion_dict['bl_c'], emotion_dict['bl_d'],
              emotion_dict['bl_e']]
        self.left_eye.set_emotion(letl, lebl)
        self.right_eye.set_emotion(retl, rebl)
        self.mouth.set_emotion(tl, bl)

    ## Integración del control
    def handle_keydown(self, key):
        action = self.key_down_event.get(key, None)
        if action:
            action()

    def handle_keypressed(self):
        """ Maneja el estado de las teclas que están pulsadas """
        keys = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas
        for key, action in self.key_pressed_events.items():
            if keys[key]:
                action()

    def space_action(self):
        self.set_emotion(self.emotion_dict_from_values(self.generate_random_vector()))
        self.logger.info("Space      key down")

    def escape_action(self):
        self.logger.info("Escape     key down")
        exit(0)

    def move_up(self):
        position = self.position
        position[1] -= self.step
        self.set_position(position)
        self.update_face()
        self.logger.info("Move up    key pressed")

    def move_down(self):
        position = self.position
        position[1] += self.step
        self.set_position(position)
        self.update_face()
        self.logger.info("Move down  key pressed")

    def move_left(self):
        position = self.position
        position[0] -= self.step
        self.set_position(position)
        self.update_face()
        self.logger.info("Move left  key pressed")

    def move_right(self):
        position = self.position
        position[0] += self.step
        self.set_position(position)
        self.update_face()
        self.logger.info("Move right key pressed")

    def increase_size(self):
        s = self.size[1]
        s += self.step
        size = [((1 + 5 ** (1 / 2)) / 2) * s, s]
        self.set_size(size)
        self.set_position(self.position)
        self.update_face()
        self.logger.info("Increase size")

    def decrease_size(self):
        s = self.size[1]
        s -= self.step
        size = [((1 + 5 ** (1 / 2)) / 2) * s, s]
        self.set_size(size)
        self.set_position(self.position)
        self.update_face()
        self.logger.info("Decrease size")


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
        screen.fill((255, 255, 255))
        hewo.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    test_component()
