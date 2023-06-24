use bevy::prelude::*;

use crate::allstructs::*;

pub fn playerlaser_enemyship_collision_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    laser_query: Query<(Entity, &Transform), With<PlayerLaser>>,
    enemy_query: Query<(Entity, &Transform), With<EnemyShip>>,
    mut events: EventWriter<CollisionEvent>,
    mut player_ship_query: Query<&mut PlayerShip>,
    audio: Res<Audio>
) {

    let explosion_sound_handle = asset_server.load("sounds/explosionsound.ogg");

    for (laser_entity, laser_transform) in laser_query.iter() {
        for (enemy_entity, enemy_transform) in enemy_query.iter() {
            if laser_collides_with_ship(laser_transform, enemy_transform) {

                // Play the explosion sound
                audio.play(explosion_sound_handle.clone());

                let explosion_position = enemy_transform.translation;
                commands.entity(laser_entity).despawn();
                commands.entity(enemy_entity).despawn();
                events.send(CollisionEvent {
                    entity1: laser_entity,
                    entity2: enemy_entity,
                    explosion: explosion_position,
                });

                for mut player_ship in player_ship_query.iter_mut() {
                    player_ship.score += 100;
                    println!("Score: {}", player_ship.score);
                    println!("");
                }

                break;
            }
        }
    }
}

pub fn enemylaser_playership_collision_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    laser_query: Query<(Entity, &Transform), With<EnemyLaser>>,
    mut player_query: Query<(&mut PlayerShip, Entity, &Transform)>,
    enemy_query: Query<Entity, With<EnemyShip>>,
    mut events: EventWriter<CollisionEvent>,
    audio: Res<Audio>, 
    mut game_over_event: EventWriter<GameOverEvent>,
) {    

    let mut player_died = false;

    let explosion_sound_handle = asset_server.load("sounds/explosionsound.ogg");
    let game_over_handle = asset_server.load("sounds/gameover.ogg");

    for (laser_entity, laser_transform) in laser_query.iter() {
        for (mut player_ship, player_entity, player_transform) in player_query.iter_mut() {
            if laser_collides_with_ship(laser_transform, player_transform) {
                
                // Play the explosion sound
                audio.play(explosion_sound_handle.clone());

                // Get the ship's position and adjust the y value so the explosion happens near the top of the player ship
                let mut explosion_position = player_transform.translation;
                explosion_position.y += 50.0;

                commands.entity(laser_entity).despawn();
                events.send(CollisionEvent {
                    entity1: laser_entity,
                    entity2: player_entity,
                    explosion: explosion_position,
                });

                player_ship.health -= 20;
                println!("Health: {}", player_ship.health); // Print health value to the console
                println!("");

                if player_ship.health <= 0 {
                    commands.entity(player_entity).despawn(); // Despawn player ship
                    audio.play(game_over_handle.clone()); // Play game over sound
                    player_died = true;
                    println!("You died! Game Over!");
                    println!("Closing game...");

                    // If player ship is dead/despawned, despawn all enemy ships
                    for enemy_entity in enemy_query.iter() {
                        commands.entity(enemy_entity).despawn();
                    }
                    break;
                }
            }
        }
    }

    if player_died {
        game_over_event.send(GameOverEvent);
    }
}

pub fn enemyships_collision_check(new_position: Vec3, query: &Query<&Transform, With<EnemyShip>>) -> bool {
    for enemy_transform in query.iter() {
        if new_position.distance(enemy_transform.translation) < 70.0 {
            return true;
        }
    }
    false
}

pub fn laser_collides_with_ship(laser_transform: &Transform, enemy_transform: &Transform) -> bool {
    let laser_position = laser_transform.translation;
    let ship_position = enemy_transform.translation;

    let distance = laser_position.distance(ship_position);
    distance < 30.0 // Distance between PlayerShip/EnemyShip and Laser
}