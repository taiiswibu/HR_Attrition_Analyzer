import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import numpy as np
from wildebeest_migration_core import WildebeestMigration, AnimalType, GRID_WIDTH, GRID_HEIGHT
from wildebeest_migration_core import SERENGETI_MAX_X, MARA_RIVER_MIN_X, MARA_RIVER_MAX_X
from wildebeest_migration_core import COLOR_WILDEBEEST_CHILD, COLOR_WILDEBEEST_ADULT, COLOR_LEADER, COLOR_LION, COLOR_CROCODILE
from wildebeest_migration_core import COLOR_SERENGETI, COLOR_MARA_RIVER, COLOR_MASAI_MARA

class WildebeestMatplotlibVisualization:
    def __init__(self):
        self.simulation = WildebeestMigration()
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.ax.set_xlim(0, GRID_WIDTH)
        self.ax.set_ylim(0, GRID_HEIGHT)
        self.ax.set_aspect('equal')
        self.ax.set_title('Wildebeest Migration Simulation - Massive Scale (2000x1600)', fontsize=16)
        
        # Set up the plot
        self.setup_zones()
        self.animal_plots = {}
        self.stats_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                      verticalalignment='top', fontsize=10, 
                                      bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Create legend
        self.create_legend()
        
    def setup_zones(self):
        """Draw the zone backgrounds"""
        # Serengeti (brown)
        serengeti_rect = Rectangle((0, 0), SERENGETI_MAX_X, GRID_HEIGHT, 
                                 facecolor=self.rgb_to_matplotlib(COLOR_SERENGETI), 
                                 alpha=0.3, label='Serengeti')
        self.ax.add_patch(serengeti_rect)
        
        # Mara River (blue)
        river_rect = Rectangle((MARA_RIVER_MIN_X, 0), MARA_RIVER_MAX_X - MARA_RIVER_MIN_X, GRID_HEIGHT,
                             facecolor=self.rgb_to_matplotlib(COLOR_MARA_RIVER), 
                             alpha=0.3, label='Mara River')
        self.ax.add_patch(river_rect)
        
        # Masai Mara (green)
        mara_rect = Rectangle((MARA_RIVER_MAX_X, 0), GRID_WIDTH - MARA_RIVER_MAX_X, GRID_HEIGHT,
                            facecolor=self.rgb_to_matplotlib(COLOR_MASAI_MARA), 
                            alpha=0.3, label='Masai Mara')
        self.ax.add_patch(mara_rect)
        
        # Add zone labels
        self.ax.text(SERENGETI_MAX_X/2, GRID_HEIGHT*0.9, 'Serengeti', 
                    ha='center', va='center', fontsize=14, fontweight='bold')
        self.ax.text((MARA_RIVER_MIN_X + MARA_RIVER_MAX_X)/2, GRID_HEIGHT*0.9, 'Mara River', 
                    ha='center', va='center', fontsize=14, fontweight='bold')
        self.ax.text((MARA_RIVER_MAX_X + GRID_WIDTH)/2, GRID_HEIGHT*0.9, 'Masai Mara', 
                    ha='center', va='center', fontsize=14, fontweight='bold')
        
    def rgb_to_matplotlib(self, rgb_color):
        """Convert RGB tuple to matplotlib color"""
        return (rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        
    def create_legend(self):
        """Create legend for animal types"""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.rgb_to_matplotlib(COLOR_WILDEBEEST_CHILD), 
                       markersize=8, label='Wildebeest Child (20px/1.0m)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.rgb_to_matplotlib(COLOR_WILDEBEEST_ADULT), 
                       markersize=10, label='Wildebeest Adult (30px/1.5m)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.rgb_to_matplotlib(COLOR_LEADER), 
                       markersize=12, label='Leader (34px/1.7m)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.rgb_to_matplotlib(COLOR_LION), 
                       markersize=14, label='Lion (40px/2.0m)'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=self.rgb_to_matplotlib(COLOR_CROCODILE), 
                       markersize=16, label='Crocodile (100px/5.0m)')
        ]
        
        self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 0.85))
        
    def update_plot(self):
        """Update the plot with current simulation state"""
        # Clear previous animal plots
        for plots in self.animal_plots.values():
            for plot in plots:
                plot.remove()
        self.animal_plots.clear()
        
        # Group animals by type
        animal_groups = {
            AnimalType.WILDEBEEST_CHILD: [],
            AnimalType.WILDEBEEST_ADULT: [],
            AnimalType.LEADER: [],
            AnimalType.LION: [],
            AnimalType.CROCODILE: []
        }
        
        for animal in self.simulation.animals:
            if animal.alive:
                animal_groups[animal.animal_type].append(animal)
        
        # Plot each animal type
        for animal_type, animals in animal_groups.items():
            if not animals:
                continue
                
            x_coords = [animal.x for animal in animals]
            y_coords = [animal.y for animal in animals]
            
            if animal_type == AnimalType.WILDEBEEST_CHILD:
                scatter = self.ax.scatter(x_coords, y_coords, 
                                        c=[self.rgb_to_matplotlib(COLOR_WILDEBEEST_CHILD)]*len(animals),
                                        s=20, alpha=0.8, edgecolors='black', linewidth=0.5)
            elif animal_type == AnimalType.WILDEBEEST_ADULT:
                scatter = self.ax.scatter(x_coords, y_coords, 
                                        c=[self.rgb_to_matplotlib(COLOR_WILDEBEEST_ADULT)]*len(animals),
                                        s=30, alpha=0.8, edgecolors='black', linewidth=0.5)
            elif animal_type == AnimalType.LEADER:
                scatter = self.ax.scatter(x_coords, y_coords, 
                                        c=[self.rgb_to_matplotlib(COLOR_LEADER)]*len(animals),
                                        s=40, alpha=0.9, edgecolors='black', linewidth=1)
            elif animal_type == AnimalType.LION:
                scatter = self.ax.scatter(x_coords, y_coords, 
                                        c=[self.rgb_to_matplotlib(COLOR_LION)]*len(animals),
                                        s=50, alpha=0.9, edgecolors='black', linewidth=1)
            elif animal_type == AnimalType.CROCODILE:
                scatter = self.ax.scatter(x_coords, y_coords, 
                                        c=[self.rgb_to_matplotlib(COLOR_CROCODILE)]*len(animals),
                                        s=100, alpha=0.9, edgecolors='black', linewidth=1, marker='s')
            
            if animal_type not in self.animal_plots:
                self.animal_plots[animal_type] = []
            self.animal_plots[animal_type].append(scatter)
        
        # Update statistics
        stats = self.simulation.get_statistics()
        stats_text = f"""Time Step: {stats['time_step']}
Total Animals: {stats['alive_animals']}/{stats['total_animals']}
Wildebeest - Children: {stats['wildebeest_children']}, Adults: {stats['wildebeest_adults']}, Leaders: {stats['leaders']}
Predators - Lions: {stats['lions']}, Crocodiles: {stats['crocodiles']}
Zones - Serengeti: {stats['animals_in_serengeti']}, River: {stats['animals_in_river']}, Masai Mara: {stats['animals_in_masai_mara']}
Deaths: {stats['dead_animals']}
Survival Rate: {stats['alive_animals']/stats['total_animals']*100:.1f}%"""
        
        self.stats_text.set_text(stats_text)
        
    def animate(self, frame):
        """Animation function for matplotlib"""
        self.simulation.update()
        self.update_plot()
        return []
        
    def save_snapshot(self, filename='wildebeest_migration_snapshot.png'):
        """Save a snapshot of the current state"""
        self.update_plot()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Snapshot saved as {filename}")
        
    def run_animation(self, frames=500, interval=100):
        """Run the animated simulation"""
        anim = animation.FuncAnimation(self.fig, self.animate, frames=frames, 
                                     interval=interval, blit=False, repeat=True)
        plt.show()
        return anim
        
    def run_static_simulation(self, steps=100):
        """Run simulation and show static snapshots"""
        print("Running static simulation...")
        
        # Initial state
        self.update_plot()
        plt.savefig('wildebeest_migration_initial.png', dpi=300, bbox_inches='tight')
        
        # Run simulation
        for i in range(steps):
            self.simulation.update()
            
            # Save snapshots at key intervals
            if i in [9, 19, 29, 49, 99]:  # Steps 10, 20, 30, 50, 100
                self.update_plot()
                plt.savefig(f'wildebeest_migration_step_{i+1:03d}.png', dpi=300, bbox_inches='tight')
                stats = self.simulation.get_statistics()
                print(f"Step {i+1:3d}: {stats['alive_animals']:3d} alive, "
                      f"Masai Mara: {stats['animals_in_masai_mara']:3d}, "
                      f"Deaths: {stats['dead_animals']:3d}")
        
        # Final state
        self.update_plot()
        plt.savefig('wildebeest_migration_final.png', dpi=300, bbox_inches='tight')
        
        final_stats = self.simulation.get_statistics()
        print(f"\nFinal Results:")
        print(f"  Migration Success: {final_stats['animals_in_masai_mara']} animals reached Masai Mara")
        print(f"  Survival Rate: {final_stats['alive_animals']/final_stats['total_animals']*100:.1f}%")
        print(f"  Snapshots saved: initial, step_010, step_020, step_030, step_050, step_100, final")
        
        plt.show()

if __name__ == "__main__":
    # Create visualization
    viz = WildebeestMatplotlibVisualization()
    
    # Run static simulation (easier to see results)
    viz.run_static_simulation(steps=100)
    
    # Uncomment to run animated version (requires display)
    # viz.run_animation(frames=100, interval=200)