/**
* Name: Elephant Migration Experiment Configuration
* Description: Additional experimental scenarios for elephant migration
* Author: Võ Văn Tài
* Tags: experiment, configuration, scenarios
*/

model elephant_migration_config

import "elephant_migration.gaml"

experiment basic_migration type: gui {
    parameter "Population size" var: nb_elephants init: 10 min: 5 max: 20;
    parameter "Predator density" var: nb_lions init: 1 min: 0 max: 3;
    parameter "River danger" var: nb_crocodiles init: 1 min: 0 max: 2;
    
    output {
        display "Migration Journey" {
            grid landscape lines: #black;
            species elephant aspect: default;
            species lion aspect: default;
            species crocodile aspect: default;
        }
        
        monitor "Success Rate" value: length(elephant where (each.alive and each.location.x >= 35)) / nb_elephants * 100;
        monitor "Journey Progress" value: mean(elephant where (each.alive) collect (each.location.x / 60 * 100));
    }
}

experiment harsh_conditions type: gui {
    parameter "Large herd" var: nb_elephants init: 25;
    parameter "Many predators" var: nb_lions init: 3;
    parameter "Dangerous river" var: nb_crocodiles init: 2;
    parameter "Fast seasons" var: season_duration init: 50;
    
    output {
        display "Harsh Migration" {
            grid landscape lines: #black;
            species elephant aspect: default;
            species lion aspect: default;
            species crocodile aspect: default;
        }
        
        monitor "Survival Rate" value: length(elephant where (each.alive)) / nb_elephants * 100;
        monitor "Mortality Causes" value: total_deaths > 0 ? "Starvation/Exhaustion" : "None";
    }
}

experiment peaceful_journey type: gui {
    parameter "Small herd" var: nb_elephants init: 8;
    parameter "No predators" var: nb_lions init: 0;
    parameter "Safe river" var: nb_crocodiles init: 0;
    parameter "Stable seasons" var: season_duration init: 150;
    
    output {
        display "Peaceful Migration" {
            grid landscape lines: #black;
            species elephant aspect: default;
        }
        
        monitor "Birth Rate" value: total_births;
        monitor "Population Growth" value: length(elephant where (each.alive)) - nb_elephants;
    }
}

experiment custom_scenario type: gui {
    parameter "Custom elephants" var: nb_elephants init: 15 min: 3 max: 50;
    parameter "Custom lions" var: nb_lions init: 2 min: 0 max: 10;
    parameter "Custom crocodiles" var: nb_crocodiles init: 1 min: 0 max: 5;
    parameter "Custom season length" var: season_duration init: 100 min: 30 max: 300;
    
    output {
        display "Custom Migration Scenario" {
            grid landscape lines: #black;
            species elephant aspect: default;
            species lion aspect: default;
            species crocodile aspect: default;
        }
        
        display "Detailed Statistics" {
            chart "Migration Progress" type: series {
                data "Elephants in West" value: length(elephant where (each.alive and each.location.x < 25)) color: #brown;
                data "Elephants in River" value: length(elephant where (each.alive and each.location.x >= 25 and each.location.x < 35)) color: #blue;
                data "Elephants in East" value: length(elephant where (each.alive and each.location.x >= 35)) color: #green;
            }
            
            chart "Health Metrics" type: series {
                data "Average Energy" value: length(elephant where (each.alive)) > 0 ? mean(elephant where (each.alive) collect each.energy) : 0 color: #orange;
                data "Average Hunger" value: length(elephant where (each.alive)) > 0 ? mean(elephant where (each.alive) collect each.hunger) : 0 color: #red;
            }
        }
        
        monitor "🌍 Current Season" value: migration_season = 0 ? "🌵 Dry Season" : "🌧️ Rainy Season";
        monitor "🐘 Population Status" value: string(length(elephant where (each.alive))) + " alive / " + string(nb_elephants) + " total";
        monitor "🏆 Migration Success" value: string(elephants_reached_east) + " elephants reached fertile lands";
        monitor "👶 Demographics" value: string(length(elephant where (each.alive and each.baby))) + " babies, " + string(length(elephant where (each.alive and each.leader))) + " leaders";
    }
}