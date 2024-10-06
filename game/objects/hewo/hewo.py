import pygame
import logging
from game.objects.hewo.face import Face
from game.settings import SettingsLoader

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(name)s: %(message)s')
logger = logging.getLogger(__name__)


class HeWo(Face):
    def __init__(self, settings=None):
        self.settings = settings
        if self.settings is None:
            self.settings = SettingsLoader().load_settings("game.settings.hewo")
            logger.info("using default settings")
        super().__init__(settings=self.settings)
        self.key_stroke = 0

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)
        # Pres space to change emotion
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print('-' * 20)
            emotion_dict = self.get_emotion()
            print('Old emotion:', self.key_stroke, list(emotion_dict.values()))
            emotion_dict['letl_a'] += 1
            print('New emotion:', self.key_stroke, list(emotion_dict.values()))
            self.set_emotion(emotion_dict)
            emotion_dict = self.get_emotion()
            print('After set:  ', self.key_stroke, list(emotion_dict.values()))
            self.key_stroke += 1

    def get_emotion(self):
        letl = self.left_eye_settings['top_lash']['emotion']
        lebl = self.left_eye_settings['bot_lash']['emotion']
        retl = self.right_eye_settings['top_lash']['emotion']
        rebl = self.right_eye_settings['bot_lash']['emotion']
        tl = self.mouth_settings['upper_lip']['emotion']
        bl = self.mouth_settings['lower_lip']['emotion']
        emotion_dict = {
            'letl_a': letl[0], 'letl_b': letl[1], 'letl_c': letl[2],
            'lebl_a': lebl[0], 'lebl_b': lebl[1], 'lebl_c': lebl[2],
            'retl_a': retl[0], 'retl_b': retl[1], 'retl_c': retl[2],
            'rebl_a': rebl[0], 'rebl_b': rebl[1], 'rebl_c': rebl[2],
            'tl_a': tl[0], 'tl_b': tl[1], 'tl_c': tl[2], 'tl_d': tl[3], 'tl_e': tl[4],
            'bl_a': bl[0], 'bl_b': bl[1], 'bl_c': bl[2], 'bl_d': bl[3], 'bl_e': bl[4]
        }
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
        print(letl)
        self.left_eye_settings['top_lash']['emotion'] = letl
        print(self.left_eye_settings['top_lash']['emotion'])
        self.left_eye_settings['bot_lash']['emotion'] = rebl
        self.right_eye_settings['top_lash']['emotion'] = retl
        self.right_eye_settings['bot_lash']['emotion'] = rebl
        self.mouth_settings['upper_lip']['emotion'] = tl
        self.mouth_settings['lower_lip']['emotion'] = bl
        self.set_face_elements()


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
