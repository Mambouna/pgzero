import pygame
from . import game


class World:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._actors = set()

    @property
    def x(self):
        """X position offset of the world. If the screen is thought of as a
        camera view looking onto the world, this controls the horizontal
        movement of the camera."""
        return self._x

    @x.setter
    def x(self, val):
        if type(val) == int :
            self._x = val
        else:
            raise TypeError("X coordinate of the world must be an integer, "
                            "not {}.".format(type(val)))

    @property
    def y(self):
        """Y position offset of the world. If the screen is thought of as a
        camera view looking onto the world, this controls the vertical
        movement of the camera."""
        return self._y

    @y.setter
    def y(self, val):
        if type(val) == int:
            self._y = val
        else:
            raise TypeError("Y coordinate of the world must be an integer, "
                            "not {}.".format(type(val)))

    @property
    def actors(self):
        """Returns a tuple of the actors in the world so they can't be
        manipulated without the use of the proper functions but can still
        be checked or iterated over."""
        return tuple(self._actors)

    def add_actors(self, *actors):
        """Adds all given actors to the world actor set or warns if they
        are already part of it. Also errors if non-actor values are given."""
        for actor in actors:
            if not type(actor) == Actor:
                raise TypeError("The world can only be given actors to track,"
                                " not {}".format(type(actor)))
            elif actor not in self._actors:
                self._actors.add(actor)
            else:
                print("WARNING: Actor is already part of the world.")

    def add_actor(self, actor):
        """QOL function to have a more natural naming for operations on 
        single actors."""
        self.add_actors(actor)

    def remove_actors(self, *actors):
        """Removes all given actors from the world actor set or warns if they
        are not part of it. Also errors if non-actor values are given."""
        for actor in actors:
            if not type(actor) == Actor:
                raise TypeError("The world only contains actors, can't remove"
                                " element of type {}".format(type(actor)))
            elif actor in self._actors:
                self._actors.remove(actor)
            else:
                print("WARNING: Actor is not part of the world, thus can't"
                      " be removed.")

    def remove_actor(self, actor):
        """QOL function to have a more natural naming for operations on 
        single actors."""
        self.remove_actors(actor)

    def draw(self):
        """Draws all actors in the world onto the screen, offset by the 
        world position."""
        for a in self._actors:
            a_surf = a._build_transformed_surf()
            tlx, tly = a.topleft
            tlx += self._x
            tly -= self._y

            game.screen.blit(a_surf, (tlx, tly))


world_instance = World()
