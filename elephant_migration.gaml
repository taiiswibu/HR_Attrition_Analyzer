/**
* Name: Elephant Migration Simulation
* Description: Realistic elephant herd migration from arid west to fertile east
* Author: Võ Văn Tài
* Tags: ecology, migration, elephant, herd, survival
*/

model elephant_migration

global {
    // Environment parameters
    int grid_width <- 60;
    int grid_height <- 40;
    
    // Population parameters
    int nb_elephants <- 15;
    int nb_lions <- 2;
    int nb_crocodiles <- 1;
    
    // Migration parameters
    int migration_season <- 0; // 0: dry season, 1: rainy season
    int season_duration <- 100;
    int cycle_count <- 0;
    
    // Statistics - Focus on migration journey
    int elephants_reached_east <- 0;
    int migration_attempts <- 0;
    int herd_cohesion <- 100;
    float average_nutrition <- 0.0;
    int total_births <- 0;
    int total_deaths <- 0;
    
    init {
        // Create landscape
        ask landscape {
            do setup_terrain;
        }
        
        // Create elephant herd - start in arid west
        create elephant number: nb_elephants {
            location <- one_of(landscape where (grid_x <= 15 and each.terrain_type = "arid"));
            if (self = first(elephant)) {
                leader <- true;
                color <- #yellow;
            } else {
                leader <- false;
                if (flip(0.2)) {
                    baby <- true;
                    color <- #pink;
                } else {
                    color <- #gray;
                }
            }
            energy <- 60 + rnd(40);
            hunger <- 20 + rnd(20);
            memory <- [location];
        }
        
        // Create lions only in arid and river zones
        create lion number: nb_lions {
            location <- one_of(landscape where (grid_x <= 35 and each.terrain_type != "fertile"));
        }
        
        // Create crocodiles only in river center
        create crocodile number: nb_crocodiles {
            location <- one_of(landscape where (each.river and grid_x > 28 and grid_x < 32));
        }
        
        write "🐘 Elephant migration simulation started!";
        write "🌍 Environment: Arid West → River → Fertile East";
    }
    
    reflex seasonal_cycle {
        cycle_count <- cycle_count + 1;
        
        if (cycle_count mod season_duration = 0) {
            migration_season <- 1 - migration_season;
            if (migration_season = 0) {
                write "🌵 Dry season begins - vegetation decreases";
            } else {
                write "🌧️ Rainy season begins - vegetation recovers";
            }
        }
        
        do update_statistics;
    }
    
    action update_statistics {
        list<elephant> alive_elephants <- elephant where (each.alive);
        
        if (length(alive_elephants) > 0) {
            average_nutrition <- mean(alive_elephants collect each.energy);
            
            // Calculate herd cohesion
            point herd_center <- mean(alive_elephants collect each.location);
            float avg_distance <- mean(alive_elephants collect (each.location distance_to herd_center));
            herd_cohesion <- int(100 - min(100, avg_distance * 5));
            
            // Count elephants in fertile east
            elephants_reached_east <- length(alive_elephants where (each.location.x >= 35));
        }
    }
}

// Landscape grid
grid landscape width: grid_width height: grid_height {
    int vegetation <- 0;
    bool water_source <- false;
    bool river <- false;
    string terrain_type <- "arid";
    
    action setup_terrain {
        // Western arid zone (x: 0-25)
        if (grid_x <= 25) {
            vegetation <- 5 + rnd(25);  // 5-30% vegetation
            water_source <- flip(0.01); // 1% water sources
            terrain_type <- "arid";
        }
        // River zone (x: 25-35)
        else if (grid_x > 25 and grid_x < 35) {
            river <- true;
            vegetation <- 20 + rnd(20);
            terrain_type <- "river";
        }
        // Eastern fertile zone (x: 35-60)
        else if (grid_x >= 35) {
            vegetation <- 60 + rnd(40);  // 60-100% vegetation
            water_source <- flip(0.08);  // 8% water sources
            terrain_type <- "fertile";
        }
        
        do update_color;
    }
    
    action update_color {
        if (water_source) {
            color <- #blue;
        } else if (river) {
            color <- #lightblue;
        } else {
            // Gradient from brown (arid) to green (fertile)
            float fertility_ratio <- vegetation / 100.0;
            int red_val <- int(139 - (fertility_ratio * 105));   // 139 → 34
            int green_val <- int(69 + (fertility_ratio * 70));   // 69 → 139
            int blue_val <- int(19 + (fertility_ratio * 15));    // 19 → 34
            color <- rgb(red_val, green_val, blue_val);
        }
    }
    
    reflex seasonal_vegetation_change {
        if (migration_season = 0) {  // Dry season
            if (terrain_type = "arid") {
                vegetation <- max(0, vegetation - rnd(3));  // Rapid decrease
            } else if (terrain_type = "fertile") {
                vegetation <- max(40, vegetation - rnd(1)); // Slow decrease
            }
        } else {  // Rainy season
            if (terrain_type = "arid") {
                vegetation <- min(30, vegetation + rnd(2)); // Slow increase
            } else if (terrain_type = "fertile") {
                vegetation <- min(100, vegetation + rnd(4)); // Fast increase
            }
        }
        do update_color;
    }
}

// Elephant species
species elephant {
    bool alive <- true;
    bool leader <- false;
    bool baby <- false;
    int energy <- 100;
    int hunger <- 0;
    int age <- 0;
    point target;
    bool migration_decision <- false;
    list<point> memory;
    
    reflex aging {
        age <- age + 1;
        if (baby and age > 200) {
            baby <- false;
        }
    }
    
    reflex evaluate_migration_need when: leader and alive {
        // Evaluate current area quality
        int local_vegetation <- 0;
        int local_water <- 0;
        
        // Check within radius of 10 cells
        loop cell over: landscape where (self distance_to each.location < 10) {
            local_vegetation <- local_vegetation + cell.vegetation;
            if (cell.water_source) {
                local_water <- local_water + 1;
            }
        }
        
        // Migration decision if conditions are poor
        if (local_vegetation < 200 and local_water < 2 and hunger > 40) {
            migration_decision <- true;
            migration_attempts <- migration_attempts + 1;
            write "🐘 Herd decides to migrate to find better lands!";
        }
        
        // Find target location
        if (migration_decision) {
            list<landscape> fertile_areas <- landscape where (each.terrain_type = "fertile" and each.vegetation > 50);
            if (length(fertile_areas) > 0) {
                target <- one_of(fertile_areas).location;
            }
        }
    }
    
    reflex maintain_herd_formation when: alive and !leader {
        // Maintain distance with herd
        list<elephant> nearby_elephants <- elephant where (each.alive and self distance_to each.location < 8);
        
        if (length(nearby_elephants) = 0) {
            // Find herd if lost
            list<elephant> herd <- elephant where (each.alive and each.leader);
            if (length(herd) > 0) {
                target <- first(herd).location;
                write "🐘 Lost elephant searching for herd!";
            }
        }
    }
    
    reflex move when: alive {
        if (target != nil) {
            do goto target: target speed: baby ? 0.5 : 1.0;
            
            // Update memory trail
            memory <- memory + [location];
            if (length(memory) > 20) {
                memory <- memory[1..19];
            }
            
            // Check if reached fertile area
            if (location.x >= 35 and !migration_decision) {
                write "🎉 Elephant reached the fertile lands!";
            }
        }
    }
    
    reflex eat when: alive {
        landscape current_cell <- landscape(location);
        if (current_cell.vegetation > 0) {
            int food_consumed <- min(current_cell.vegetation, 10);
            current_cell.vegetation <- current_cell.vegetation - food_consumed;
            energy <- min(100, energy + food_consumed);
            hunger <- max(0, hunger - food_consumed);
        }
        
        if (current_cell.water_source) {
            energy <- min(100, energy + 5);
            hunger <- max(0, hunger - 5);
        }
    }
    
    reflex lose_energy when: alive {
        energy <- energy - (baby ? 0.5 : 1.0);
        hunger <- hunger + (baby ? 0.5 : 1.0);
        
        if (energy <= 0 or hunger >= 100) {
            alive <- false;
            total_deaths <- total_deaths + 1;
            write "💀 An elephant has died from exhaustion or hunger";
        }
    }
    
    reflex reproduction when: alive and !baby and energy > 80 and age > 300 {
        if (flip(0.001)) {  // Very low birth rate
            create elephant number: 1 {
                location <- myself.location;
                baby <- true;
                color <- #pink;
                energy <- 60;
                hunger <- 20;
                memory <- [location];
            }
            total_births <- total_births + 1;
            write "🐣 A baby elephant was born!";
        }
    }
    
    aspect default {
        if (alive) {
            rgb elephant_color <- leader ? #yellow : (baby ? #pink : #gray);
            
            // Size changes based on energy
            float health_ratio <- energy / 100.0;
            float base_size <- baby ? 1.5 : (leader ? 2.8 : 2.0);
            float actual_size <- base_size * (0.6 + 0.4 * health_ratio);
            
            draw circle(actual_size) color: elephant_color;
            
            // Display movement trail
            if (length(memory) > 1) {
                draw line(memory) color: #gray width: 1;
            }
        } else {
            draw circle(1.0) color: #black;
        }
    }
}

// Lion species
species lion {
    bool alive <- true;
    int energy <- 100;
    point target;
    
    reflex hunt when: alive {
        list<elephant> nearby_elephants <- elephant where (each.alive and self distance_to each.location < 5);
        if (length(nearby_elephants) > 0) {
            target <- one_of(nearby_elephants).location;
        }
    }
    
    reflex move when: alive and target != nil {
        do goto target: target speed: 1.5;
    }
    
    reflex lose_energy when: alive {
        energy <- energy - 1;
        if (energy <= 0) {
            alive <- false;
        }
    }
    
    aspect default {
        if (alive) {
            draw circle(2.0) color: #orange;
        }
    }
}

// Crocodile species
species crocodile {
    bool alive <- true;
    int energy <- 100;
    
    reflex attack when: alive {
        list<elephant> nearby_elephants <- elephant where (each.alive and self distance_to each.location < 3);
        if (length(nearby_elephants) > 0) {
            elephant target_elephant <- one_of(nearby_elephants);
            target_elephant.energy <- target_elephant.energy - 20;
            energy <- min(100, energy + 10);
            write "🐊 Crocodile attacks elephant in the river!";
        }
    }
    
    reflex lose_energy when: alive {
        energy <- energy - 0.5;
        if (energy <= 0) {
            alive <- false;
        }
    }
    
    aspect default {
        if (alive) {
            draw circle(2.5) color: #darkgreen;
        }
    }
}

experiment elephant_migration_experiment type: gui {
    parameter "Number of elephants" var: nb_elephants min: 5 max: 30 category: "Population";
    parameter "Number of lions" var: nb_lions min: 0 max: 5 category: "Population";
    parameter "Number of crocodiles" var: nb_crocodiles min: 0 max: 3 category: "Population";
    parameter "Season duration" var: season_duration min: 50 max: 200 category: "Environment";
    
    output {
        display main_display {
            grid landscape lines: #black;
            species elephant aspect: default;
            species lion aspect: default;
            species crocodile aspect: default;
        }
        
        display chart_display {
            chart "Migration Statistics" type: series {
                data "Elephants in Fertile East" value: elephants_reached_east color: #green;
                data "Migration Attempts" value: migration_attempts color: #blue;
                data "Herd Cohesion %" value: herd_cohesion color: #yellow;
            }
            
            chart "Population Health" type: series {
                data "Average Nutrition" value: average_nutrition color: #orange;
                data "Total Births" value: total_births color: #pink;
                data "Total Deaths" value: total_deaths color: #red;
            }
        }
        
        monitor "🏆 Elephants in Fertile East" value: elephants_reached_east;
        monitor "🚶 Migration Attempts" value: migration_attempts;
        monitor "🤝 Herd Cohesion (%)" value: herd_cohesion;
        monitor "🍃 Average Nutrition" value: average_nutrition;
        monitor "🐣 Total Births" value: total_births;
        monitor "💀 Total Deaths" value: total_deaths;
        monitor "🌍 Season" value: migration_season = 0 ? "Dry" : "Rainy";
        monitor "🐘 Alive Elephants" value: length(elephant where (each.alive));
    }
}