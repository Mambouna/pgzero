import pygame
import pygame.mouse
from collections import deque
from itertools import islice
from . import loaders


class Mouse:
    """Interface to the pygame mouse. Also integrates former
    enum properties of mouse to retain all previous functionality
    and be backwards compatible.
    """

    def __init__(self):
        self._pressed = [False, False, False]
        self._pos = None
        self._rel = (0, 0)
        self._last_pos = (0, 0)
        self._last_rel = (0, 0)
        self._recent_pos = deque(maxlen=60)
        self._recent_rel = deque(maxlen=60)

    def _press(self, button):
        self._pressed[button - 1] = True

    def _release(self, button):
        self._pressed[button - 1] = False

    def _set_pos(self, pos):
        self._pos = pos
        self._recent_pos.appendleft(pos)

    def _add_rel(self, rel):
        self._rel = self._rel[0] + rel[0], self._rel[1] + rel[1]
        lrx = self._last_rel[0] + rel[0]
        lry = self._last_rel[1] + rel[1]
        self._last_rel = lrx, lry
        self._recent_rel.appendleft(rel)

    def _null_rel(self):
        self._rel = (0, 0)

    @property
    def LEFT(self):
        return 1

    @property
    def MIDDLE(self):
        return 2

    @property
    def RIGHT(self):
        return 3

    @property
    def WHEEL_UP(self):
        return 4

    @property
    def WHEEL_DOWN(self):
        return 5

    # TODO: Clean up the return value of this to make it easier
    # to understand for users.
    @property
    def pressed(self):
        return tuple(self._pressed)

    @property
    def pressed_left(self):
        return self._pressed[0]

    @property
    def pressed_middle(self):
        return self._pressed[1]

    @property
    def pressed_right(self):
        return self._pressed[2]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos, pos_y=None):
        # Setting mouse visibility is a workaround to allow
        # setting the mouse position under Wayland, which
        # normally prevents user applications from doing this.
        # switch_back is necessary in case the pointer is
        # moved while already set invisible by the user.
        switch_back = True if self.visible else False
        pygame.mouse.set_visible(False)
        if pos_y:
            pygame.mouse.set_pos([pos, pos_y])
        # TODO: Nicer way to do this? Does it have to be so strict
        # in checking?
        elif isinstance(pos, (tuple, list)) and len(pos) == 2 and\
                isinstance(pos[0], int) and isinstance(pos[1], int):
            pygame.mouse.set_pos(pos)
        else:
            raise ValueError("Setting the mouse position requires either"
                             " one tuple with two integers or two integers"
                             " as individual parameters.")
        if switch_back:
            pygame.mouse.set_visible(True)
        # Note: Setting self._pos manually here isn't necessary
        # because set_pos() triggers a new MOUSEMOTION event.

    @property
    def last_called_pos(self):
        p = self._last_pos
        self._last_pos = self._pos
        return p

    @property
    def recent_pos(self):
        return tuple(self._recent_pos)

    @property
    def recent_pos_max(self):
        return self._recent_pos.maxlen

    @recent_pos_max.setter
    def recent_pos_max(self, maxl):
        c_max = self._recent_pos.maxlen
        if maxl > c_max:
            self._recent_pos = deque(self._recent_pos, maxlen=maxl)
        elif maxl < c_max:
            elems = islice(self._recent_pos, maxl)
            self._recent_pos = deque(elems, maxlen=maxl)

    @property
    def rel(self):
        return self._rel

    @property
    def last_called_rel(self):
        r = self._last_rel
        self._last_rel = (0, 0)
        return r

    @property
    def recent_rel(self):
        return tuple(self._recent_rel)

    @property
    def recent_rel_max(self):
        return self._recent_rel.maxlen

    @recent_rel_max.setter
    def recent_rel_max(self, maxl):
        c_max = self._recent_rel.maxlen
        if maxl > c_max:
            self._recent_rel = deque(self._recent_rel, maxlen=maxl)
        elif maxl < c_max:
            elems = islice(self._recent_rel, maxl)
            self._recent_rel = deque(elems, maxlen=maxl)

    @property
    def visible(self):
        return pygame.mouse.get_visible()

    @visible.setter
    def visible(self, val):
        match val:
            case bool():
                vis = val
            case 0:
                vis = False
            case 1:
                vis = True
            case _:
                raise ValueError("Value to set mouse visibility must be"
                                 " a boolean or either 1 or 0.")
        pygame.mouse.set_visible(vis)

    @property
    def focused(self):
        return pygame.mouse.get_focused()


mouse_instance = Mouse()
