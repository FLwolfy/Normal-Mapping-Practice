import core.Config as Config
import numpy
import pygame

class Tile:
    def __init__(self, world_coords: tuple[int,int,int], height: float):
        self.color = (0,0,0)
        self.world_coords = world_coords
        self.rect = pygame.Rect(world_coords[0], world_coords[1], Config.TILE_SIZE, Config.TILE_SIZE)
        self.normal_vector = numpy.array([0, 0, 1])
        '''
        This the normal vector of the tile based on the right-side tile and down-side tile next to it.
        '''
        self.__height = height
        self.__raw_color = Config.TILE_COLOR
    
    @property
    def height(self) -> float:
        return self.__height
    
    @property
    def raw_color(self) -> tuple[int,int,int]:
        return self.__raw_color
        
