import os
import pygame
import logging
import screeninfo
from game.settings.settings_loader import SettingsLoader
from game.objects.hewo.face import Face

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(name)s: %(message)s')

class MainWindow:
    def __init__(self, settings, layout_list=None, active_layout=None):
        # Cargar configuración
        pygame.init()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.settings = settings
        monitors = screeninfo.get_monitors()
        self.logger.info(f"Monitors: {[(m.name, m.width, m.height) for m in monitors]}")

        if self.settings['deploy']:
            flags = pygame.RESIZABLE | pygame.FULLSCREEN
            monitor_id = self.settings['monitor_id']
            monitor_specs = monitors[monitor_id]
            self.window_size = (monitor_specs.width, monitor_specs.height)
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_specs.x},{monitor_specs.y}"
        else:
            flags = pygame.RESIZABLE
            monitor_id = self.settings['monitor_id']
            monitor_specs = monitors[monitor_id]
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_specs.x - monitor_specs.width/2},{monitor_specs.y}"
            self.window_size = (self.settings['width'], self.settings['height'])
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            display=monitor_id,
            flags=flags,
            vsync=True
        )

        pygame.display.set_caption(self.settings['window_title'])
        self.layout_list = layout_list
        self.clock = pygame.time.Clock()
        self.background_color = self.settings['bg_color']
        self.active_layout = active_layout

    def handle_events(self):
        for event in pygame.event.get():
            # Define window events
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()
                exit()

            # Pass the event_handler to the active canvas
            if self.active_layout is not None:
                self.layout_list[self.active_layout].draw(self.screen)

    def set_active_layout(self, layout_index):
        if layout_index < len(self.layout_list):
            self.active_layout = layout_index
        else:
            self.active_layout = None
            print(f'Index {layout_index} out of range')

    def update(self):
        if self.active_layout is not None:
            self.layout_list[self.active_layout].draw(self.screen)

    def draw(self):
        self.screen.fill(self.background_color)
        if self.active_layout is not None:
            self.layout_list[self.active_layout].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

def main():
    window_settings = SettingsLoader().load_settings("game.settings.window")
    print(window_settings)
    hewo_face_settings = SettingsLoader().load_settings("game.settings.hewo")
    print(hewo_face_settings)
    main_window = MainWindow(settings=window_settings, layout_list=[Face()], active_layout=0)
    main_window.run()

if __name__ == '__main__':
    main()