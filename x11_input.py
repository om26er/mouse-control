from time import sleep

from Xlib import display, X
from Xlib.ext.xtest import fake_input


_PRESSED_KEYS = []
_PRESSED_MOUSE_BUTTONS = []


class Mouse:

    def __init__(self):
        super().__init__()
        self.display = display.Display()
        screen_data = self.display.screen()._data
        self.screen_height = screen_data['height_in_pixels']
        self.screen_width = screen_data['width_in_pixels']

    @property
    def x(self):
        return self.position()[0]

    @property
    def y(self):
        return self.position()[1]

    def _press(self, button=1):
        _PRESSED_MOUSE_BUTTONS.append(button)
        fake_input(self.display, X.ButtonPress, button)
        self.display.sync()

    def _release(self, button=1):
        if button in _PRESSED_MOUSE_BUTTONS:
            _PRESSED_MOUSE_BUTTONS.remove(button)
        fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()

    def click(self, button=1, press_duration=0.10):
        self._press(button)
        sleep(press_duration)
        self._release(button)

    def move(self, percent_x, percent_y, velocity=0.1):

        if percent_x < -100 or percent_x > 100:
            raise ValueError("Value of percent_x must be between -100 and 100")

        if percent_y < -100 or percent_y > 100:
            raise ValueError("Value of percent_y must be between -100 and 100")

        if velocity <= 0 or velocity > 10:
            raise ValueError("Value of velocity must be between 0.1 and 10.0")

        pixels_x = int((percent_x / 100) * self.screen_width)
        pixels_y = int((percent_y / 100) * self.screen_height)

        steps = int(100 / velocity)

        for i in range(steps):
            fake_input(self.display, X.MotionNotify, True, x=int(pixels_x / steps),
                       y=int(pixels_y / steps))
            self.display.sync()
            sleep(0.01)

    def position(self):
        coord = self.display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]


if __name__ == '__main__':
    mouse = Mouse()
    mouse.move(100, -100, 1)
    mouse.click()
