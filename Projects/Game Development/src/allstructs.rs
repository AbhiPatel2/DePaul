use bevy::prelude::*;

#[derive(Component)]
pub struct PlayerShip {
    pub speed: f32,
    pub movement_range: f32,
    pub health: i32,
    pub score: i32
}

#[derive(Component)]
pub struct EnemyShip;

#[derive(Component)]
pub struct PlayerLaser;

#[derive(Component)]
pub struct Velocity(pub Vec3);

#[derive(Component)]
pub struct PlayerShootLaserState {
    pub space_pressed: bool,
}
impl Default for PlayerShootLaserState {
    fn default() -> Self {
        PlayerShootLaserState { space_pressed: false }
    }
}

#[derive(Component)]
pub struct EnemyLaser;

pub struct CollisionEvent {
    pub entity1: Entity,
    pub entity2: Entity,
    pub explosion: Vec3
}

#[derive(Component)]
pub struct Explosion;

#[derive(Component)]
pub struct ExplosionTimer(pub Timer);

pub struct GameOverEvent;