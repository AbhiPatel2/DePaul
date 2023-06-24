use bevy::prelude::*;

use crate::allstructs::*;

pub fn explosion_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    time: Res<Time>,
    _timer: Local<Timer>,
    mut collision_event_reader: EventReader<CollisionEvent>,
    mut query: Query<(Entity, &mut ExplosionTimer)>,
) {
    for event in collision_event_reader.iter() {

        commands
            .spawn(SpriteBundle {
                texture: asset_server.load("sprites/explosion.png"),
                transform: Transform {
                    translation: event.explosion,
                    scale: Vec3::splat(0.35),
                    ..Default::default()
                },
                ..Default::default()
            })
            .insert(Explosion {})
            .insert(ExplosionTimer(Timer::from_seconds(0.25, TimerMode::Once)));
    }

    for (entity, mut timer) in query.iter_mut() {
        timer.0.tick(time.delta());

        if timer.0.finished() {
            commands.entity(entity).despawn();
        }
    }
}