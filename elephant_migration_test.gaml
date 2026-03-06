/**
* Name: Elephant Migration Test
* Description: Basic validation tests for the elephant migration simulation
* Author: Võ Văn Tài
* Tags: test, validation, unit-test
*/

model elephant_migration_test

import "elephant_migration.gaml"

experiment validation_tests type: gui {
    parameter "Test elephants" var: nb_elephants init: 5;
    parameter "Test lions" var: nb_lions init: 1;
    parameter "Test crocodiles" var: nb_crocodiles init: 1;
    parameter "Test season length" var: season_duration init: 50;
    
    init {
        write "🧪 Starting Elephant Migration Validation Tests";
        write "=========================================";
    }
    
    reflex test_environment_setup when: cycle = 1 {
        write "🌍 Testing Environment Setup:";
        
        // Test arid zone
        list<landscape> arid_cells <- landscape where (each.terrain_type = "arid");
        bool arid_test_passed <- length(arid_cells) > 0;
        write "   - Arid zone created: " + (arid_test_passed ? "✅ PASS" : "❌ FAIL");
        
        // Test river zone
        list<landscape> river_cells <- landscape where (each.terrain_type = "river");
        bool river_test_passed <- length(river_cells) > 0;
        write "   - River zone created: " + (river_test_passed ? "✅ PASS" : "❌ FAIL");
        
        // Test fertile zone
        list<landscape> fertile_cells <- landscape where (each.terrain_type = "fertile");
        bool fertile_test_passed <- length(fertile_cells) > 0;
        write "   - Fertile zone created: " + (fertile_test_passed ? "✅ PASS" : "❌ FAIL");
        
        // Test vegetation gradient
        float avg_arid_vegetation <- mean(arid_cells collect each.vegetation);
        float avg_fertile_vegetation <- mean(fertile_cells collect each.vegetation);
        bool vegetation_gradient_test <- avg_fertile_vegetation > avg_arid_vegetation;
        write "   - Vegetation gradient: " + (vegetation_gradient_test ? "✅ PASS" : "❌ FAIL");
        write "     (Arid: " + avg_arid_vegetation + ", Fertile: " + avg_fertile_vegetation + ")";
    }
    
    reflex test_elephant_creation when: cycle = 1 {
        write "🐘 Testing Elephant Population:";
        
        // Test elephant count
        list<elephant> all_elephants <- elephant where (each.alive);
        bool count_test_passed <- length(all_elephants) = nb_elephants;
        write "   - Elephant count: " + (count_test_passed ? "✅ PASS" : "❌ FAIL");
        write "     (Expected: " + nb_elephants + ", Actual: " + length(all_elephants) + ")";
        
        // Test leader assignment
        list<elephant> leaders <- elephant where (each.leader and each.alive);
        bool leader_test_passed <- length(leaders) = 1;
        write "   - Leader assignment: " + (leader_test_passed ? "✅ PASS" : "❌ FAIL");
        write "     (Leaders: " + length(leaders) + ")";
        
        // Test baby elephants
        list<elephant> babies <- elephant where (each.baby and each.alive);
        bool baby_test_passed <- length(babies) >= 0;
        write "   - Baby elephants: " + (baby_test_passed ? "✅ PASS" : "❌ FAIL");
        write "     (Babies: " + length(babies) + ")";
        
        // Test starting location (should be in arid zone)
        bool location_test_passed <- true;
        loop elephant_agent over: all_elephants {
            if (elephant_agent.location.x > 25) {
                location_test_passed <- false;
            }
        }
        write "   - Starting location: " + (location_test_passed ? "✅ PASS" : "❌ FAIL");
    }
    
    reflex test_predator_creation when: cycle = 1 {
        write "🦁 Testing Predator Population:";
        
        // Test lion count
        list<lion> all_lions <- lion where (each.alive);
        bool lion_count_test <- length(all_lions) = nb_lions;
        write "   - Lion count: " + (lion_count_test ? "✅ PASS" : "❌ FAIL");
        
        // Test crocodile count
        list<crocodile> all_crocodiles <- crocodile where (each.alive);
        bool crocodile_count_test <- length(all_crocodiles) = nb_crocodiles;
        write "   - Crocodile count: " + (crocodile_count_test ? "✅ PASS" : "❌ FAIL");
        
        // Test crocodile location (should be in river)
        bool croc_location_test <- true;
        loop crocodile_agent over: all_crocodiles {
            landscape croc_cell <- landscape(crocodile_agent.location);
            if (!croc_cell.river) {
                croc_location_test <- false;
            }
        }
        write "   - Crocodile location: " + (croc_location_test ? "✅ PASS" : "❌ FAIL");
    }
    
    reflex test_seasonal_effects when: cycle = 100 {
        write "🌦️ Testing Seasonal Effects:";
        
        // Test season change
        bool season_change_test <- migration_season = 1; // Should have changed after 50 cycles
        write "   - Season change: " + (season_change_test ? "✅ PASS" : "❌ FAIL");
        write "     (Current season: " + (migration_season = 0 ? "Dry" : "Rainy") + ")";
        
        // Test vegetation change
        list<landscape> arid_cells <- landscape where (each.terrain_type = "arid");
        float avg_arid_vegetation <- mean(arid_cells collect each.vegetation);
        bool vegetation_change_test <- avg_arid_vegetation < 30; // Should be low in arid areas
        write "   - Vegetation dynamics: " + (vegetation_change_test ? "✅ PASS" : "❌ FAIL");
        write "     (Arid vegetation: " + avg_arid_vegetation + ")";
    }
    
    reflex test_elephant_behavior when: cycle = 150 {
        write "🐘 Testing Elephant Behavior:";
        
        // Test elephant movement
        list<elephant> moving_elephants <- elephant where (each.alive and length(each.memory) > 1);
        bool movement_test <- length(moving_elephants) > 0;
        write "   - Elephant movement: " + (movement_test ? "✅ PASS" : "❌ FAIL");
        
        // Test energy consumption
        list<elephant> all_elephants <- elephant where (each.alive);
        float avg_energy <- mean(all_elephants collect each.energy);
        bool energy_test <- avg_energy < 100; // Should have consumed some energy
        write "   - Energy consumption: " + (energy_test ? "✅ PASS" : "❌ FAIL");
        write "     (Average energy: " + avg_energy + ")";
        
        // Test migration decision
        bool migration_test <- migration_attempts > 0;
        write "   - Migration decision: " + (migration_test ? "✅ PASS" : "❌ FAIL");
        write "     (Migration attempts: " + migration_attempts + ")";
    }
    
    reflex test_statistics when: cycle = 200 {
        write "📊 Testing Statistics:";
        
        // Test statistic calculation
        bool stats_test <- average_nutrition >= 0 and herd_cohesion >= 0;
        write "   - Statistics calculation: " + (stats_test ? "✅ PASS" : "❌ FAIL");
        write "     (Avg nutrition: " + average_nutrition + ", Cohesion: " + herd_cohesion + "%)";
        
        // Test elephant tracking
        list<elephant> alive_elephants <- elephant where (each.alive);
        bool tracking_test <- length(alive_elephants) <= nb_elephants;
        write "   - Population tracking: " + (tracking_test ? "✅ PASS" : "❌ FAIL");
        write "     (Alive: " + length(alive_elephants) + "/" + nb_elephants + ")";
        
        write "=========================================";
        write "🎯 Test Summary Complete - Cycle " + cycle;
    }
    
    output {
        display "Test Visualization" {
            grid landscape lines: #black;
            species elephant aspect: default;
            species lion aspect: default;
            species crocodile aspect: default;
        }
        
        monitor "🧪 Test Status" value: "Running validation tests...";
        monitor "⏱️ Test Cycle" value: cycle;
        monitor "🐘 Elephants Alive" value: length(elephant where (each.alive));
        monitor "🏆 Migration Success" value: elephants_reached_east;
        monitor "📊 Statistics Valid" value: average_nutrition >= 0 and herd_cohesion >= 0;
    }
}