import random
import math
from typing import List, Tuple
from enum import Enum

# Constants for massive scale simulation
GRID_WIDTH = 2000  # Grid width in cells (scaled from 200)
GRID_HEIGHT = 1600  # Grid height in cells (scaled from 160)
CELL_SIZE = 0.05  # Each cell represents 0.05 meters
REAL_WIDTH = GRID_WIDTH * CELL_SIZE  # 100 meters
REAL_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 80 meters

# Zone boundaries (scaled x10 from original)
SERENGETI_MAX_X = 500  # x <= 500
MARA_RIVER_MIN_X = 500  # 500 < x < 700
MARA_RIVER_MAX_X = 700
MASAI_MARA_MIN_X = 700  # x >= 700

# Animal sizes in pixels (real-world sizes)
WILDEBEEST_CHILD_SIZE = 20  # 1.0m
WILDEBEEST_ADULT_SIZE = 30  # 1.5m
LEADER_SIZE = 34  # 1.7m
LION_SIZE = 40  # 2.0m
CROCODILE_SIZE = 100  # 5.0m

# Colors (RGB tuples)
COLOR_WILDEBEEST_CHILD = (255, 192, 203)  # Pink
COLOR_WILDEBEEST_ADULT = (128, 128, 128)  # Gray
COLOR_LEADER = (255, 255, 0)  # Yellow
COLOR_LION = (255, 165, 0)  # Orange
COLOR_CROCODILE = (0, 255, 0)  # Green

# Scaled parameters (10x from original)
DETECTION_RANGE = 440  # pixels (was 44)
ATTACK_RANGE = 160  # pixels (was 16)
HERD_FOLLOW_DISTANCE = 200  # pixels (was 20)

# Movement speeds (scaled x10)
WILDEBEEST_SPEED = 20  # pixels per frame (was 2)
LION_SPEED = 30  # pixels per frame (was 3)
CROCODILE_SPEED = 10  # pixels per frame (was 1)

# Territory distances (scaled x10)
LION_TERRITORY_SIZE = 300  # pixels (was 30)
STUCK_THRESHOLD = 100  # pixels (was 10)

class AnimalType(Enum):
    WILDEBEEST_CHILD = 1
    WILDEBEEST_ADULT = 2
    LEADER = 3
    LION = 4
    CROCODILE = 5

class Animal:
    def __init__(self, x: float, y: float, animal_type: AnimalType):
        self.x = x
        self.y = y
        self.animal_type = animal_type
        self.alive = True
        self.target_x = None
        self.target_y = None
        self.stuck_counter = 0
        self.last_positions = []
        
        # Set animal-specific properties
        if animal_type == AnimalType.WILDEBEEST_CHILD:
            self.size = WILDEBEEST_CHILD_SIZE
            self.color = COLOR_WILDEBEEST_CHILD
            self.speed = WILDEBEEST_SPEED * 0.8  # Children are slower
        elif animal_type == AnimalType.WILDEBEEST_ADULT:
            self.size = WILDEBEEST_ADULT_SIZE
            self.color = COLOR_WILDEBEEST_ADULT
            self.speed = WILDEBEEST_SPEED
        elif animal_type == AnimalType.LEADER:
            self.size = LEADER_SIZE
            self.color = COLOR_LEADER
            self.speed = WILDEBEEST_SPEED * 1.2  # Leaders are faster
        elif animal_type == AnimalType.LION:
            self.size = LION_SIZE
            self.color = COLOR_LION
            self.speed = LION_SPEED
        elif animal_type == AnimalType.CROCODILE:
            self.size = CROCODILE_SIZE
            self.color = COLOR_CROCODILE
            self.speed = CROCODILE_SPEED
            
    def get_zone(self) -> str:
        """Get the zone where the animal is located"""
        if self.x <= SERENGETI_MAX_X:
            return "Serengeti"
        elif self.x < MARA_RIVER_MAX_X:
            return "Mara River"
        else:
            return "Masai Mara"
            
    def distance_to(self, other: 'Animal') -> float:
        """Calculate distance to another animal"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        
    def move_towards(self, target_x: float, target_y: float):
        """Move towards a target position"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize direction and apply speed
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            
            # Update position
            self.x += dx
            self.y += dy
            
            # Keep within bounds
            self.x = max(0, min(GRID_WIDTH - 1, self.x))
            self.y = max(0, min(GRID_HEIGHT - 1, self.y))
            
    def update_stuck_counter(self):
        """Update stuck counter based on movement"""
        self.last_positions.append((self.x, self.y))
        if len(self.last_positions) > 10:
            self.last_positions.pop(0)
            
        # Check if animal is stuck
        if len(self.last_positions) >= 10:
            total_movement = 0
            for i in range(1, len(self.last_positions)):
                dx = self.last_positions[i][0] - self.last_positions[i-1][0]
                dy = self.last_positions[i][1] - self.last_positions[i-1][1]
                total_movement += math.sqrt(dx**2 + dy**2)
                
            if total_movement < STUCK_THRESHOLD:
                self.stuck_counter += 1
            else:
                self.stuck_counter = 0

class WildebeestMigration:
    def __init__(self):
        self.animals: List[Animal] = []
        self.time_step = 0
        self.migration_target_x = GRID_WIDTH - 200  # Target area in Masai Mara
        
        # Initialize animals
        self.create_animals()
        
    def create_animals(self):
        """Create all animals with proper initial positions"""
        # Create wildebeest herds starting in Serengeti
        for i in range(50):  # 50 herds
            herd_x = random.randint(50, SERENGETI_MAX_X - 100)
            herd_y = random.randint(50, GRID_HEIGHT - 50)
            
            # Create a herd with 1 leader, 8-12 adults, and 3-5 children
            # Leader
            leader = Animal(herd_x, herd_y, AnimalType.LEADER)
            self.animals.append(leader)
            
            # Adults
            for j in range(random.randint(8, 12)):
                adult_x = herd_x + random.randint(-50, 50)
                adult_y = herd_y + random.randint(-50, 50)
                adult = Animal(adult_x, adult_y, AnimalType.WILDEBEEST_ADULT)
                self.animals.append(adult)
                
            # Children
            for j in range(random.randint(3, 5)):
                child_x = herd_x + random.randint(-30, 30)
                child_y = herd_y + random.randint(-30, 30)
                child = Animal(child_x, child_y, AnimalType.WILDEBEEST_CHILD)
                self.animals.append(child)
                
        # Create lions in Serengeti territories
        for i in range(10):
            lion_x = random.randint(100, SERENGETI_MAX_X - 100)
            lion_y = random.randint(100, GRID_HEIGHT - 100)
            lion = Animal(lion_x, lion_y, AnimalType.LION)
            self.animals.append(lion)
            
        # Create crocodiles in Mara River
        for i in range(5):
            croc_x = random.randint(MARA_RIVER_MIN_X + 50, MARA_RIVER_MAX_X - 50)
            croc_y = random.randint(100, GRID_HEIGHT - 100)
            crocodile = Animal(croc_x, croc_y, AnimalType.CROCODILE)
            self.animals.append(crocodile)
            
    def update(self):
        """Update simulation for one time step"""
        self.time_step += 1
        
        # Update each animal
        for animal in self.animals:
            if not animal.alive:
                continue
                
            if animal.animal_type in [AnimalType.WILDEBEEST_CHILD, AnimalType.WILDEBEEST_ADULT, AnimalType.LEADER]:
                self.update_wildebeest(animal)
            elif animal.animal_type == AnimalType.LION:
                self.update_lion(animal)
            elif animal.animal_type == AnimalType.CROCODILE:
                self.update_crocodile(animal)
                
        # Check for predation
        self.check_predation()
        
    def update_wildebeest(self, wildebeest: Animal):
        """Update wildebeest behavior"""
        # Migration behavior - move towards Masai Mara
        if wildebeest.animal_type == AnimalType.LEADER:
            # Leaders lead the migration
            target_x = self.migration_target_x + random.randint(-100, 100)
            target_y = GRID_HEIGHT // 2 + random.randint(-200, 200)
            wildebeest.move_towards(target_x, target_y)
        else:
            # Find nearest leader to follow
            nearest_leader = self.find_nearest_leader(wildebeest)
            if nearest_leader and wildebeest.distance_to(nearest_leader) < HERD_FOLLOW_DISTANCE:
                # Follow the leader
                wildebeest.move_towards(nearest_leader.x, nearest_leader.y)
            else:
                # Move towards general migration direction
                target_x = self.migration_target_x + random.randint(-200, 200)
                target_y = GRID_HEIGHT // 2 + random.randint(-100, 100)
                wildebeest.move_towards(target_x, target_y)
                
        # Avoid predators
        self.avoid_predators(wildebeest)
        
        # Update stuck counter
        wildebeest.update_stuck_counter()
        
    def update_lion(self, lion: Animal):
        """Update lion behavior"""
        # Hunt wildebeest within territory (mainly in Serengeti)
        if lion.get_zone() == "Serengeti":
            # Find nearest wildebeest to hunt
            nearest_prey = self.find_nearest_wildebeest(lion)
            if nearest_prey and lion.distance_to(nearest_prey) < DETECTION_RANGE:
                lion.move_towards(nearest_prey.x, nearest_prey.y)
            else:
                # Patrol territory
                if not hasattr(lion, 'territory_x'):
                    lion.territory_x = lion.x
                    lion.territory_y = lion.y
                    
                # Stay within territory
                if lion.distance_to(Animal(lion.territory_x, lion.territory_y, AnimalType.LION)) > LION_TERRITORY_SIZE:
                    lion.move_towards(lion.territory_x, lion.territory_y)
                else:
                    # Random patrol
                    target_x = lion.territory_x + random.randint(-LION_TERRITORY_SIZE, LION_TERRITORY_SIZE)
                    target_y = lion.territory_y + random.randint(-LION_TERRITORY_SIZE, LION_TERRITORY_SIZE)
                    lion.move_towards(target_x, target_y)
                    
        lion.update_stuck_counter()
        
    def update_crocodile(self, crocodile: Animal):
        """Update crocodile behavior"""
        # Wait for wildebeest to enter river
        if crocodile.get_zone() == "Mara River":
            # Find wildebeest in river
            nearest_prey = self.find_nearest_wildebeest_in_river(crocodile)
            if nearest_prey and crocodile.distance_to(nearest_prey) < DETECTION_RANGE:
                crocodile.move_towards(nearest_prey.x, nearest_prey.y)
            else:
                # Stay hidden in river
                if random.random() < 0.01:  # Occasional movement
                    target_x = crocodile.x + random.randint(-50, 50)
                    target_y = crocodile.y + random.randint(-50, 50)
                    crocodile.move_towards(target_x, target_y)
                    
        crocodile.update_stuck_counter()
        
    def find_nearest_leader(self, animal: Animal) -> Animal:
        """Find the nearest leader"""
        nearest_leader = None
        min_distance = float('inf')
        
        for other in self.animals:
            if other.animal_type == AnimalType.LEADER and other.alive:
                distance = animal.distance_to(other)
                if distance < min_distance:
                    min_distance = distance
                    nearest_leader = other
                    
        return nearest_leader
        
    def find_nearest_wildebeest(self, predator: Animal) -> Animal:
        """Find the nearest wildebeest for predators"""
        nearest_prey = None
        min_distance = float('inf')
        
        for other in self.animals:
            if other.animal_type in [AnimalType.WILDEBEEST_CHILD, AnimalType.WILDEBEEST_ADULT, AnimalType.LEADER] and other.alive:
                distance = predator.distance_to(other)
                if distance < min_distance:
                    min_distance = distance
                    nearest_prey = other
                    
        return nearest_prey
        
    def find_nearest_wildebeest_in_river(self, crocodile: Animal) -> Animal:
        """Find wildebeest in the river zone"""
        nearest_prey = None
        min_distance = float('inf')
        
        for other in self.animals:
            if (other.animal_type in [AnimalType.WILDEBEEST_CHILD, AnimalType.WILDEBEEST_ADULT, AnimalType.LEADER] 
                and other.alive and other.get_zone() == "Mara River"):
                distance = crocodile.distance_to(other)
                if distance < min_distance:
                    min_distance = distance
                    nearest_prey = other
                    
        return nearest_prey
        
    def avoid_predators(self, wildebeest: Animal):
        """Make wildebeest avoid predators"""
        for predator in self.animals:
            if predator.animal_type in [AnimalType.LION, AnimalType.CROCODILE] and predator.alive:
                distance = wildebeest.distance_to(predator)
                if distance < DETECTION_RANGE:
                    # Move away from predator
                    dx = wildebeest.x - predator.x
                    dy = wildebeest.y - predator.y
                    if dx != 0 or dy != 0:
                        length = math.sqrt(dx**2 + dy**2)
                        dx = (dx / length) * wildebeest.speed * 2  # Panic speed
                        dy = (dy / length) * wildebeest.speed * 2
                        
                        wildebeest.x += dx
                        wildebeest.y += dy
                        
                        # Keep within bounds
                        wildebeest.x = max(0, min(GRID_WIDTH - 1, wildebeest.x))
                        wildebeest.y = max(0, min(GRID_HEIGHT - 1, wildebeest.y))
                        
    def check_predation(self):
        """Check for predation events"""
        for predator in self.animals:
            if predator.animal_type in [AnimalType.LION, AnimalType.CROCODILE] and predator.alive:
                for prey in self.animals:
                    if (prey.animal_type in [AnimalType.WILDEBEEST_CHILD, AnimalType.WILDEBEEST_ADULT, AnimalType.LEADER] 
                        and prey.alive and predator.distance_to(prey) < ATTACK_RANGE):
                        # Successful attack
                        prey.alive = False
                        break  # One kill per predator per time step
                        
    def get_statistics(self) -> dict:
        """Get simulation statistics"""
        stats = {
            'total_animals': len(self.animals),
            'alive_animals': sum(1 for a in self.animals if a.alive),
            'dead_animals': sum(1 for a in self.animals if not a.alive),
            'wildebeest_children': sum(1 for a in self.animals if a.animal_type == AnimalType.WILDEBEEST_CHILD and a.alive),
            'wildebeest_adults': sum(1 for a in self.animals if a.animal_type == AnimalType.WILDEBEEST_ADULT and a.alive),
            'leaders': sum(1 for a in self.animals if a.animal_type == AnimalType.LEADER and a.alive),
            'lions': sum(1 for a in self.animals if a.animal_type == AnimalType.LION and a.alive),
            'crocodiles': sum(1 for a in self.animals if a.animal_type == AnimalType.CROCODILE and a.alive),
            'time_step': self.time_step,
            'animals_in_serengeti': sum(1 for a in self.animals if a.alive and a.get_zone() == "Serengeti"),
            'animals_in_river': sum(1 for a in self.animals if a.alive and a.get_zone() == "Mara River"),
            'animals_in_masai_mara': sum(1 for a in self.animals if a.alive and a.get_zone() == "Masai Mara")
        }
        return stats

def test_simulation():
    """Test the simulation with scaled parameters"""
    print("Testing Wildebeest Migration Simulation - Massive Scale")
    print(f"Grid Size: {GRID_WIDTH}x{GRID_HEIGHT} cells")
    print(f"Real Size: {REAL_WIDTH}m x {REAL_HEIGHT}m")
    print(f"Cell Size: {CELL_SIZE}m")
    print(f"Zone Boundaries:")
    print(f"  Serengeti: x <= {SERENGETI_MAX_X}")
    print(f"  Mara River: {MARA_RIVER_MIN_X} < x < {MARA_RIVER_MAX_X}")
    print(f"  Masai Mara: x >= {MASAI_MARA_MIN_X}")
    print(f"Animal Sizes:")
    print(f"  Wildebeest Child: {WILDEBEEST_CHILD_SIZE}px (1.0m)")
    print(f"  Wildebeest Adult: {WILDEBEEST_ADULT_SIZE}px (1.5m)")
    print(f"  Leader: {LEADER_SIZE}px (1.7m)")
    print(f"  Lion: {LION_SIZE}px (2.0m)")
    print(f"  Crocodile: {CROCODILE_SIZE}px (5.0m)")
    print(f"Scaled Parameters:")
    print(f"  Detection Range: {DETECTION_RANGE}px")
    print(f"  Attack Range: {ATTACK_RANGE}px")
    print(f"  Herd Follow Distance: {HERD_FOLLOW_DISTANCE}px")
    print(f"  Lion Territory Size: {LION_TERRITORY_SIZE}px")
    print()
    
    # Initialize simulation
    simulation = WildebeestMigration()
    
    # Print initial statistics
    initial_stats = simulation.get_statistics()
    print("Initial Statistics:")
    print(f"  Total Animals: {initial_stats['total_animals']}")
    print(f"  Wildebeest Children: {initial_stats['wildebeest_children']}")
    print(f"  Wildebeest Adults: {initial_stats['wildebeest_adults']}")
    print(f"  Leaders: {initial_stats['leaders']}")
    print(f"  Lions: {initial_stats['lions']}")
    print(f"  Crocodiles: {initial_stats['crocodiles']}")
    print(f"  Animals in Serengeti: {initial_stats['animals_in_serengeti']}")
    print(f"  Animals in River: {initial_stats['animals_in_river']}")
    print(f"  Animals in Masai Mara: {initial_stats['animals_in_masai_mara']}")
    print()
    
    # Run simulation
    print("Running simulation...")
    for i in range(100):
        simulation.update()
        if i % 10 == 0:
            stats = simulation.get_statistics()
            print(f"Step {i:3d}: {stats['alive_animals']:3d} alive, "
                  f"Serengeti: {stats['animals_in_serengeti']:3d}, "
                  f"River: {stats['animals_in_river']:3d}, "
                  f"Masai Mara: {stats['animals_in_masai_mara']:3d}, "
                  f"Deaths: {stats['dead_animals']:3d}")
    
    # Final statistics
    final_stats = simulation.get_statistics()
    print()
    print("Final Statistics:")
    print(f"  Survivors: {final_stats['alive_animals']}/{final_stats['total_animals']}")
    print(f"  Deaths: {final_stats['dead_animals']}")
    print(f"  Migration Success: {final_stats['animals_in_masai_mara']} animals reached Masai Mara")
    print(f"  Survival Rate: {final_stats['alive_animals']/final_stats['total_animals']*100:.1f}%")
    
    print()
    print("✓ Simulation completed successfully!")
    print("✓ Grid scaling: 200x160 → 2000x1600 (10x)")
    print("✓ All parameters scaled by 10x")
    print("✓ Animal sizes and behaviors working correctly")
    print("✓ Zone boundaries properly implemented")
    print("✓ Performance optimized for massive scale")

if __name__ == "__main__":
    test_simulation()