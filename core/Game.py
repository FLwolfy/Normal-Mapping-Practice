from core.Tilemap import Tilemap
import pygame
import core.Config as Config

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Initialize instances
        self.map = Tilemap()

    # Main loop
    def run(self):
        clock = pygame.time.Clock()
        timer = 1000
        timer_max = int(Config.FRAME_RATE * Config.DAY_PERIOD / 6)
        timer_offset = timer / timer_max
        timer_direction = 1
        
        running = True
        is_paused = False
        while running:
            # Frame rates
            clock.tick(Config.FRAME_RATE)
            
            # Handling event
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                elif (event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_RETURN):
                        self.map.do_show_normal = not self.map.do_show_normal
                        self.map.update_day_light(timer / timer_max - timer_offset)
                        self.map.draw()
                        pygame.display.update()
                    elif(event.key == pygame.K_SPACE):
                        is_paused = not is_paused
                    elif(event.key == pygame.K_LEFT):
                        timer_direction = 1
                    elif(event.key == pygame.K_RIGHT):
                        timer_direction = -1            
            
            if(is_paused):
                continue
            
            # Light Update
            if(timer % (timer_max // 2) == 0):
                self.map.update_day_light(timer / timer_max - timer_offset)
            
            # Rendering Update
            self.map.draw()
            
            # Update display
            pygame.display.update()
            
            # Timer Update
            if(timer // timer_max >= 360):
                timer = 0
            if(timer_direction == 1):
                timer += 1
            elif(timer_direction == -1):
                timer -= 1
                        
        pygame.quit()
        


