use bevy::prelude::*;

use crate::allstructs::*;

pub fn playership_movement_system(
    keyboard_input: Res<Input<KeyCode>>,
    mut query: Query<(&mut Transform, &PlayerShip), With<PlayerShip>>,
) {
    let window_width = 800.0;

    for (mut transform, player_ship) in query.iter_mut() {
        let mut direction = 0.0;

        // Move left
        if keyboard_input.pressed(KeyCode::Left) {
            direction -= 1.0;
        }

        // Move right
        if keyboard_input.pressed(KeyCode::Right) {
            direction += 1.0;
        }

        let translation = &mut transform.translation;
        translation.x += direction * player_ship.speed;

        // Option 1 - Allow the player to go to the opposite side of the window by going out of the window width
        // Move the player ship to the opposite side of the window
        let half_width = window_width * 0.5;
        if translation.x < -half_width  {
            translation.x = half_width;
        } else if translation.x > half_width  {
            translation.x = -half_width;
        }

        // Option 2 - Limit the player's movement range so they can't go outside of the window
        /* Minimum and maximum x-axis values for player ship movement
        let min_x = -player_ship.movement_range;
        let max_x = player_ship.movement_range;
        translation.x = translation.x.min(max_x).max(min_x); */
    }
}

pub fn player_shoot_laser_system(
    asset_server: Res<AssetServer>,
    keyboard_input: Res<Input<KeyCode>>,
    mut commands: Commands,
    player_ship_query: Query<&Transform, With<PlayerShip>>,
    mut state: Local<PlayerShootLaserState>,
    audio: Res<Audio>
) {

    let laser_handle = asset_server.load("sounds/laser.ogg");

    if keyboard_input.just_released(KeyCode::Space) {
        state.space_pressed = false;
    }

    if keyboard_input.just_pressed(KeyCode::Space) && !state.space_pressed {
        state.space_pressed = true;

        audio.play(laser_handle.clone());

        for player_ship_transform in player_ship_query.iter() {
            let laser_transform = Transform {
                translation: player_ship_transform.translation,
                rotation: Quat::from_rotation_z(std::f32::consts::FRAC_PI_2),
                scale: Vec3::splat(0.45),
                ..Default::default()
            };

            let laser_velocity = Vec3::new(0.0, 550.0, 0.0);

            commands
                .spawn(SpriteBundle {
                    texture: asset_server.load("sprites/playerlaser.png"),
                    transform: laser_transform,
                    ..Default::default()
                })
                .insert(PlayerLaser)
                .insert(Velocity(laser_velocity));
        }
    }
}