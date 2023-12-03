from core.Tile import Tile
import core.Config as Config
import random
import pygame
import numpy
import noise
import math

class Tilemap: 
    def __init__(self):
        self.center_pos = (Config.WIN_WIDTH / 2 + random.randint(-200,200), Config.WIN_HEIGHT / 2 + random.randint(-200,-50))
        '''
        This is the center point of the tilemap (not the screen).
        '''
        
        self.tiles: list[list[Tile]]
        '''
        All tiles' info are stored in this 2D-list. 
        The 2D-list is like this: self.tiles[y][x] = tile
        '''
           
        self.generate_tiles()
        self.calculate_tiles_normal()
       
    def generate_tiles(self) -> None:
        map_width = Config.WIN_WIDTH // Config.TILE_SIZE
        map_height = Config.WIN_HEIGHT // Config.TILE_SIZE
        self.tiles = [[None]*map_width for _ in range(map_height)]
        for x in range(map_width):
            for y in range(map_height):
                world_coords = self.tile_coords_to_world_coords((x, y))
                height = noise.pnoise2(y / Config.NOISE_SCALE,
                                       x / Config.NOISE_SCALE, 
                                       octaves=Config.NOISE_OCTAVES, 
                                       persistence=Config.NOISE_PERSISTENCE, 
                                       lacunarity=Config.NOISE_LACUNARITY, 
                                       repeatx=1024, 
                                       repeaty=1024, 
                                       base=Config.NOISE_SEED)
                height = (height + 1) / 2 # clamp to 0-1
                
                # Initialize tile info      
                tile = Tile(world_coords, height)
                                 
                self.tiles[y][x] = tile
    
    def tile_coords_to_world_coords(self, tile_coords: tuple) -> tuple:     
        world_coords = (tile_coords[0] * Config.TILE_SIZE, tile_coords[1] * Config.TILE_SIZE)        
        return world_coords
    
    def calculate_tiles_normal(self) -> None:
        '''
        Get normal vector of all tiles based on the right-side tile and down-side tile next to the specific tile.
        '''
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[1])):
                down_vector = numpy.array([0, 1, 0])
                right_vector = numpy.array([1, 0, 0])
                
                if(y + 1 < len(self.tiles)):
                    down_vector = numpy.array([0, 1, (self.tiles[y + 1][x].height - self.tiles[y][x].height) * Config.TILE_HEIGHT_UNIT])
                if(x + 1 < len(self.tiles[1])):
                    right_vector = numpy.array([1, 0, (self.tiles[y][x + 1].height - self.tiles[y][x].height) * Config.TILE_HEIGHT_UNIT])
                    
                normal_vector = numpy.cross(right_vector, down_vector)
                normal_vector = normal_vector / numpy.linalg.norm(normal_vector)
                
                self.tiles[y][x].normal_vector = normal_vector
                
    def update_day_light(self, sun_angle: float) -> None:
        '''
        Update the daylight for the tilemap (sun_angle in radians)
        '''
        direction = numpy.array([math.cos(math.radians(sun_angle)), 0, math.sin(math.radians(sun_angle))])
        
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[1])):
                # Determine the light intensity
                cos_value = numpy.dot(self.tiles[y][x].normal_vector, direction)
                light_intensity = min(max(Config.MIN_LIGHT_INTENSITY, cos_value), Config.MAX_LIGHT_INTENSITY)
                
                # add light effect
                new_color_tile = (self.tiles[y][x].raw_color[0] * light_intensity,
                                  self.tiles[y][x].raw_color[1] * light_intensity,
                                  self.tiles[y][x].raw_color[2] * light_intensity)
                
                self.tiles[y][x].color = new_color_tile
                           
    def draw_color(self, sun_angle: float) -> None:
        self.update_day_light(sun_angle)
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[1])):
                tile = self.tiles[y][x]
                pygame.draw.rect(Config.WIN, tile.color, tile.rect)   
                
    def draw_normal(self) -> None:
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[1])):
                tile = self.tiles[y][x]
                
                # get normal color
                normal_color = (int((tile.normal_vector[0] + 1) / 2 * 255),
                                int((tile.normal_vector[1] + 1) / 2 * 255),
                                int((tile.normal_vector[2] + 1) / 2 * 255))
                pygame.draw.rect(Config.WIN, normal_color, tile.rect)    