from pyboy import WindowEvent


class Action():

    def __init__(self, start_event, end_event, s):
        self._start_event = start_event
        self._end_event = end_event
        self._s = s

    def perform_action(self, pyboy, tick_count=24):
        legit_ticks = max(24, tick_count)
        pyboy.send_input(self._start_event)
        for _ in range(12):
            pyboy.tick()
        pyboy.send_input(self._end_event)
        for _ in range(legit_ticks-12):
            pyboy.tick()

    @property
    def name(self):
        return self._s


ACTION_UP = Action(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP, "Up")
ACTION_DOWN = Action(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN, "Down")
ACTION_LEFT = Action(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT, "Left")
ACTION_RIGHT = Action(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT, "Right")

ACTION_A = Action(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A, "A")
ACTION_B = Action(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B, "B")
ACTION_START = Action(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START, "Start")
ACTION_SELECT = Action(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT, "Select")

ALL_VALID_ACTIONS = [
    ACTION_UP,
    ACTION_DOWN,
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_A,
    ACTION_B,
    ACTION_START,
    ACTION_SELECT
]

