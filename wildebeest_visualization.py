import pygame
import sys
from wildebeest_migration import WildebeestMigration, AnimalType, GRID_WIDTH, GRID_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, SCALE_FACTOR
from wildebeest_migration import SERENGETI_MAX_X, MARA_RIVER_MIN_X, MARA_RIVER_MAX_X, MASAI_MARA_MIN_X
from wildebeest_migration import COLOR_SERENGETI, COLOR_MARA_RIVER, COLOR_MASAI_MARA

class WildebeestVisualization:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT + 100))  # Extra space for stats
        pygame.display.set_caption("Wildebeest Migration Simulation - Massive Scale (2000x1600)")
        self.clock = pygame.time.Clock()
        self.simulation = WildebeestMigration()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)
        self.paused = False
        self.running = True
        
    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates"""
        screen_x = int(x * SCALE_FACTOR)
        screen_y = int(y * SCALE_FACTOR)
        return screen_x, screen_y
        
    def draw_zones(self):
        """Draw the different zones (Serengeti, Mara River, Masai Mara)"""
        # Serengeti (brown)
        serengeti_width = int(SERENGETI_MAX_X * SCALE_FACTOR)
        pygame.draw.rect(self.screen, COLOR_SERENGETI, (0, 0, serengeti_width, DISPLAY_HEIGHT))
        
        # Mara River (blue)
        river_x = int(MARA_RIVER_MIN_X * SCALE_FACTOR)
        river_width = int((MARA_RIVER_MAX_X - MARA_RIVER_MIN_X) * SCALE_FACTOR)
        pygame.draw.rect(self.screen, COLOR_MARA_RIVER, (river_x, 0, river_width, DISPLAY_HEIGHT))
        
        # Masai Mara (green)
        mara_x = int(MARA_RIVER_MAX_X * SCALE_FACTOR)
        mara_width = DISPLAY_WIDTH - mara_x
        pygame.draw.rect(self.screen, COLOR_MASAI_MARA, (mara_x, 0, mara_width, DISPLAY_HEIGHT))
        
        # Draw zone labels
        serengeti_label = self.font.render("Serengeti", True, (255, 255, 255))
        self.screen.blit(serengeti_label, (10, 10))
        
        river_label = self.font.render("Mara River", True, (255, 255, 255))
        self.screen.blit(river_label, (river_x + 10, 10))
        
        mara_label = self.font.render("Masai Mara", True, (255, 255, 255))
        self.screen.blit(mara_label, (mara_x + 10, 10))
        
    def draw_animals(self):
        """Draw all animals on the screen"""
        for animal in self.simulation.animals:
            if not animal.alive:
                continue
                
            screen_x, screen_y = self.world_to_screen(animal.x, animal.y)
            
            # Scale animal size for display
            display_size = max(2, int(animal.size * SCALE_FACTOR))
            
            # Draw animal as a circle
            pygame.draw.circle(self.screen, animal.color, (screen_x, screen_y), display_size)
            
            # Draw a small border for better visibility
            pygame.draw.circle(self.screen, (0, 0, 0), (screen_x, screen_y), display_size, 1)
            
    def draw_statistics(self):
        """Draw simulation statistics"""
        stats = self.simulation.get_statistics()
        
        # Background for statistics
        pygame.draw.rect(self.screen, (50, 50, 50), (0, DISPLAY_HEIGHT, DISPLAY_WIDTH, 100))
        
        # Create statistics text
        stats_text = [
            f"Time Step: {stats['time_step']}",
            f"Total Animals: {stats['alive_animals']}/{stats['total_animals']}",
            f"Wildebeest - Children: {stats['wildebeest_children']}, Adults: {stats['wildebeest_adults']}, Leaders: {stats['leaders']}",
            f"Predators - Lions: {stats['lions']}, Crocodiles: {stats['crocodiles']}",
            f"Zones - Serengeti: {stats['animals_in_serengeti']}, River: {stats['animals_in_river']}, Masai Mara: {stats['animals_in_masai_mara']}",
            f"Deaths: {stats['dead_animals']}"
        ]
        
        # Draw statistics
        y_offset = DISPLAY_HEIGHT + 5
        for i, text in enumerate(stats_text):
            if i < 3:
                color = (255, 255, 255)
            else:
                color = (200, 200, 200)
            rendered_text = self.small_font.render(text, True, color)
            self.screen.blit(rendered_text, (10, y_offset + i * 15))
            
        # Draw instructions
        instructions = [
            "SPACE: Pause/Resume",
            "ESC: Exit",
            "Grid: 2000x1600 (100m x 80m)"
        ]
        
        x_offset = DISPLAY_WIDTH - 250
        for i, instruction in enumerate(instructions):
            rendered_text = self.small_font.render(instruction, True, (255, 255, 0))
            self.screen.blit(rendered_text, (x_offset, y_offset + i * 15))
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def run(self):
        """Main simulation loop"""
        while self.running:
            self.handle_events()
            
            if not self.paused:
                self.simulation.update()
                
            # Clear screen
            self.screen.fill((0, 0, 0))
            
            # Draw everything
            self.draw_zones()
            self.draw_animals()
            self.draw_statistics()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualization = WildebeestVisualization()
    visualization.run()