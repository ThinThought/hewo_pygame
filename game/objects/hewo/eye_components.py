import pygame
import copy
import numpy as np
from scipy.interpolate import make_interp_spline
from game.settings import create_logger

class EyeLash:
    def __init__(self, size, position, settings, object_name="EyeLash"):
        self.logger = create_logger(object_name)
        self.settings = copy.deepcopy(settings)
        self.set_size(size)
        self.set_position(position)
        self.emotion = self.settings['emotion']
        self.color = self.settings['color']
        x, y = self.position
        w, h = self.size
        self.polygon_points = [
            [0 + x, 0 + y],
            [0 + x, h + y],
            [w / 2 + x, h + y],
            [w + x, h + y],
            [w + x, 0 + y],
            [w / 2 + x, 0 + y]
        ]
        self.flip = self.settings['flip']
        self.set_emotion(self.settings['emotion'])

    def handle_event(self, event):
        pass

    def update(self):
        self.update_polygon_points()

    def update_polygon_points(self):
        x, y = self.position
        w, h = self.size
        self.polygon_points = [
            [0 + x, 0 + y],
            [0 + x, h + y],
            [w / 2 + x, h + y],
            [w + x, h + y],
            [w + x, 0 + y],
            [w / 2 + x, 0 + y]
        ]
        indices = [1, 2, 3]
        if self.flip:
            indices = [0, 5, 4]
        for i, tup in enumerate(zip(indices, self.emotion)):
            self.polygon_points[tup[0]][1] = self.position[1] + self.size[1] * (tup[1] / 100)

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

    def draw(self, surface):
        polygon = self.create_polygon()
        pygame.draw.polygon(surface, self.color, polygon)

    def set_size(self, size):
        self.size = size
        self.max_emotion = self.size[1]
        self.logger.info(f"size set: {self.size}")

    def set_position(self, position):
        self.position = position
        self.logger.info(f"position set: {self.position}")

    def get_emotion(self):
        self.logger.debug(f"current emotion: {self.emotion}")
        return self.emotion

    def set_emotion(self, emotion):
        for i, e in enumerate(emotion):
            self.emotion[i] = max(0, min(e, 100))
        self.logger.debug(f"emotion set: {self.emotion}")


class Pupil:
    def __init__(self, size, position, settings, object_name="Pupil"):
        self.logger = create_logger(object_name)
        self.set_size(size)
        self.set_position(position)
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