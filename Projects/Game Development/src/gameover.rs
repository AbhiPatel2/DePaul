use bevy::prelude::*;
use bevy::app::AppExit;

use std::time::Duration;

use crate::allstructs::*;

pub fn game_over_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    time: Res<Time>,
    mut timer: Local<Timer>,
    mut game_over_event: EventReader<GameOverEvent>,
    mut app_exit_events: ResMut<Events<bevy::app::AppExit>>
) {
    timer.tick(time.delta());

    // Create a delay of 4 seconds after the player dies to display game over image and then close the app
    for _ in game_over_event.iter() {
        timer.reset();
        timer.set_duration(Duration::from_secs(4));

        commands
            .spawn(SpriteBundle {
                texture: asset_server.load("backgrounds/gameover.png"),
                transform: Transform {
                    scale: Vec3::splat(0.5),
                    ..Default::default()
                },
                ..Default::default()
            });
    }
    if timer.elapsed() >= Duration::from_secs(4) {
        app_exit_events.send(AppExit);
    }
}