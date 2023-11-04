from pyboy import WindowEvent

class PyBoyAction:

    def __init__(self, press_event, release_event):
        self._press = press_event
        self._release = release_event

    def perform_action(self, pyboy):

        pyboy.send_input(self.press_event)
        pyboy.tick() # Process press event
        pyboy.send_input(self.release_event)
        pyboy.tick() # Process release event


class MoveLeftAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT)

class MoveRightAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT)

class MoveUpAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP)

class MoveDownAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN)

class ButtonAAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A)

class ButtonBAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B)

class ButtonStartAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START)

class ButtonSelectAction(PyBoyAction):
    def __init__(self):
        super().__init__(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT)
