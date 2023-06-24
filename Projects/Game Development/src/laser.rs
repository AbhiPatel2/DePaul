use bevy::prelude::*;

use crate::allstructs::*;

pub fn laser_movement_system(
    time: Res<Time>,
    mut commands: Commands,
    mut query: Query<(Entity, &mut Transform, &Velocity), Or<(With<PlayerLaser>, With<EnemyLaser>)>>,
) {
    let window_height = 600.0;

    for (entity, mut transform, velocity) in query.iter_mut() {
        transform.translation += velocity.0 * time.delta_seconds();

        // Check if laser is outside the window's height
        if transform.translation.y < (-window_height * 0.5) + 20.0 || transform.translation.y > (window_height * 0.5) - 35.0 {
            // Despawn the laser if it's outside the window height
            commands.entity(entity).despawn();
        }
    }
}