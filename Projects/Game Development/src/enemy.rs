use bevy::prelude::*;
use std::time::Duration;
use rand::Rng;

use crate::allstructs::*;
use crate::collision::enemyships_collision_check;

pub fn spawn_enemyships(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    time: Res<Time>,
    mut timer: Local<Timer>,
    query: Query<&Transform, With<EnemyShip>>,
    player_query: Query<&Transform, With<PlayerShip>>,
) {
    timer.tick(time.delta());

    if !timer.finished() {
        return;
    }

    timer.reset();
    timer.set_duration(Duration::from_secs(1));

    let min_x = -750 / 2;   // Minimum x position within the window (left side)
    let max_x = 750 / 2;    // Maximum x position within the window (right side)

    let window_height = 550.0;

    let x = rand::thread_rng().gen_range(min_x..max_x) as f32;  
    let y = rand::random::<f32>() * (window_height / 2.0) - 10.0; // Only spawn in the top half of the window
    let new_position = Vec3::new(x, y, 0.0);

    // Only spawn enemies if player ship exists
    if let Some(_player_transform) = player_query.iter().next() {
        if !enemyships_collision_check(new_position, &query) {
            commands
                .spawn(SpriteBundle {
                    texture: asset_server.load("sprites/enemy.png"),
                    transform: Transform {
                        translation: new_position,
                        scale: Vec3::new(0.45, -0.45, 1.0),
                        ..Default::default()
                    },
                    ..Default::default()
                })
                .insert(EnemyShip);
        }
    }
}

pub fn enemy_shoot_laser_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    time: Res<Time>,
    mut timer: Local<Timer>,
    query: Query<&Transform, With<EnemyShip>>,
) {
    timer.tick(time.delta());

    if !timer.finished() {
        return;
    }

    timer.reset();
    timer.set_duration(Duration::from_secs(2.1 as u64)); // Time gap between each laser shot from enemy

    for enemy_transform in query.iter() {
        let laser_transform = Transform {
            translation: enemy_transform.translation,
            rotation: enemy_transform.rotation * Quat::from_rotation_z(-std::f32::consts::FRAC_PI_2), // Make enemy laser face down
            scale: Vec3::splat(0.30),
            ..Default::default()
        };

        let laser_velocity = Vec3::new(0.0, -375.0, 0.0);

        commands
            .spawn(SpriteBundle {
                texture: asset_server.load("sprites/enemylaser.png"),
                transform: laser_transform,
                ..Default::default()
            })
            .insert(EnemyLaser)
            .insert(Velocity(laser_velocity));
    }
}