/* Assets
    Backgrounds - https://wallpaper.dog/blue-and-purple-galaxy-wallpapers (background.png), https://www.vhv.rs/ (gameover.png)
    Sounds - https://mixkit.co/free-sound-effects/explosion/ (Had to convert files from .wav to .ogg)
    Sprites - https://opengameart.org/
*/

use bevy::prelude::*;

mod player; 
mod enemy;
mod laser;
mod collision;
mod explosion;
mod allstructs;
mod gameover;

use allstructs::*;

use player::playership_movement_system;
use player::player_shoot_laser_system;
use enemy::spawn_enemyships;
use enemy::enemy_shoot_laser_system;
use laser::laser_movement_system;
use collision::playerlaser_enemyship_collision_system;
use collision::enemylaser_playership_collision_system;
use gameover::game_over_system;
use explosion::explosion_system;

fn main() {

    println!("Health: 100");

    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window { 
                // Setting screen size to background size
                resolution: (800., 600.).into(),
                ..default()
            }),
            ..default()
        }))
        .add_startup_system(setup_game)
        .add_system(spawn_enemyships)
        .add_system(playership_movement_system)
        .add_system(player_shoot_laser_system)
        .add_system(laser_movement_system)
        .add_system(playerlaser_enemyship_collision_system)
        .add_system(explosion_system)
        .add_system(enemy_shoot_laser_system)
        .add_system(enemylaser_playership_collision_system)
        .add_system(game_over_system)
        .add_event::<CollisionEvent>()
        .add_event::<GameOverEvent>()
        .run();
}

fn setup_game(mut commands: Commands, asset_server: Res<AssetServer>, audio: Res<Audio>) {
    commands.spawn(Camera2dBundle::default());

    commands.spawn(SpriteBundle {
        texture: asset_server.load("backgrounds/background.png"),
        ..Default::default()
    });

    // Play game opener sound
    let game_opener_handle = asset_server.load("sounds/gameopener.ogg");
    audio.play(game_opener_handle.clone());

    commands
        .spawn(SpriteBundle {
            texture: asset_server.load("sprites/playership.png"),
            transform: Transform {
                translation: Vec3::new(0.0, -240.0, 0.0),
                scale: Vec3::splat(0.5),
                ..Default::default()
            },
            ..Default::default()
        })
        .insert(PlayerShip {
            speed: 9.0,
            movement_range: 366.0,
            health: 100,
            score: 0
        });
}
