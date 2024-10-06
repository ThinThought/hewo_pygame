import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from game.settings import create_logger
import copy


class Pupil:
    def __init__(self, size, position, settings, object_name="Pupil"):
        # TODO: Shrink the pupil to extract new emotions.
        self.logger = create_logger(object_name)
        self.size = size
        self.position = position
        self.color = settings['color']

    def update(self):
        pass

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (0, 0, self.size[0], self.size[1]))


class EyeLash:
    def __init__(self, size, position, settings, object_name="EyeLash"):
        self.logger = create_logger(object_name)
        self.settings = copy.deepcopy(settings)
        self.size = size
        self.position = position
        self.color = self.settings['color']
        self.max_emotion = self.size[1]
        self.emotion = self.settings['emotion']
        x, y = position
        w, h = size
        self.polygon_points = [
            [0 + x, 0 + y],
            [0 + x, h + y],
            [w / 2 + x, h + y],
            [w + x, h + y],
            [w + x, 0 + y],
            [w / 2 + x, 0 + y]
        ]
        self.flip = self.settings['flip']
        self.set_emotion(self.emotion)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        polygon = self.create_polygon()
        pygame.draw.polygon(surface, self.color, polygon)

    def create_polygon(self):
        points = self.polygon_points[1:4]
        if self.flip:
            points = [self.polygon_points[0], self.polygon_points[5], self.polygon_points[4]]
        ############################
        x_points = np.array([p[0] for p in points])
        y_points = np.array([p[1] for p in points])
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        interpolated_points = [(int(x), int(spline(x))) for x in x_range]
        ############################
        polygon = [self.polygon_points[0]] + interpolated_points + self.polygon_points[4:]
        if self.flip:
            interpolated_points.reverse()
            polygon = self.polygon_points[1:4] + interpolated_points
        return polygon

    def get_emotion(self):
        self.logger.debug(f"current emotion: {self.emotion}")
        return self.emotion

    def set_emotion(self, emotion):
        for i, e in enumerate(emotion):
            self.emotion[i] = max(0, min(e, 100))
        self.update_polygon_points()
        self.logger.debug(f"emotion set: {self.emotion}")

    def update_polygon_points(self):
        indices = [1, 2, 3]
        if self.flip:
            indices = [0, 5, 4]

        for i, tup in enumerate(zip(indices, self.emotion)):
            self.polygon_points[tup[0]][1] = self.position[1] + self.size[1] * (tup[1] / 100)
        self.logger.debug(f"polygon points updated: {self.polygon_points}")


class Eye:
    # Here I should initialize all the elements that make up the eye
    def __init__(self, size, position, settings, object_name="Eye"):
        self.logger = create_logger(object_name)
        self.settings = copy.deepcopy(settings)
        self.size = size
        self.position = position
        self.BG_COLOR = self.settings['bg_color']

        # Sizes are in proportion to the eye size
        self.lash_size = (self.size[0], self.size[1] / 2)
        self.t_pos = (0, 0)
        self.b_pos = (0, self.size[1] / 2)

        # Declare the elements that make up the eye
        self.top_lash = EyeLash(
            size=self.lash_size,
            position=self.t_pos,
            settings=self.settings['top_lash'],
            object_name=f"{object_name} - Top Lash"
        )
        self.pupil = Pupil(
            size=self.size,
            position=self.position,
            settings=self.settings['pupil'],
            object_name=f"{object_name} - Pupil"
        )
        self.bot_lash = EyeLash(
            size=self.lash_size,
            position=self.b_pos,
            settings=self.settings['bot_lash'],
            object_name=f"{object_name} - Bottom Lash"
        )

        # And initialize the surface of it
        self.eye_surface = pygame.Surface(self.size)

    def handle_event(self, event):
        self.top_lash.handle_event(event)
        self.pupil.handle_event(event)
        self.bot_lash.handle_event(event)

    def draw(self, surface):
        self.eye_surface = pygame.surface.Surface(self.size)
        self.eye_surface.fill(self.BG_COLOR)
        self.pupil.draw(self.eye_surface)
        self.top_lash.draw(self.eye_surface)
        self.bot_lash.draw(self.eye_surface)
        surface.blit(self.eye_surface, self.position)

    def update(self):
        self.top_lash.update()
        self.pupil.update()
        self.bot_lash.update()

    def set_emotion(self, t_emotion, b_emotion):
        self.logger.debug(f"emotion set: {t_emotion}, {b_emotion}")
        self.top_lash.set_emotion(t_emotion)
        self.bot_lash.set_emotion(b_emotion)

    def get_emotion(self):
        top_emotion = self.top_lash.get_emotion()
        bot_emotion = self.bot_lash.get_emotion()
        self.logger.debug(f"current emotion: {top_emotion}, {bot_emotion}")
        return top_emotion, bot_emotion
