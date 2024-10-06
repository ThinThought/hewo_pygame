import copy
import random
import pygame
from game.objects.hewo.face import Face
from game.settings import SettingsLoader, create_logger


class HeWo(Face):
    def __init__(self, settings, object_name="HeWo"):
        self.logger = create_logger(object_name)
        self.settings = settings
        super().__init__(settings=self.settings)
        self.key_stroke = 0

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.logger.info("Space key pressed" + "-" * 30)
            vec = self.generate_random_vector()
            self.set_emotion(self.emotion_dict_from_values(vec))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.logger.info("Escape key pressed" + "-" * 30)
            exit(0)

    def generate_random_vector(self, n=22):
        vec = [random.randint(0, 100) for _ in range(n)]
        self.logger.info("Generating random emotion vector")
        return [random.randint(0, 100) for _ in range(n)]

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
