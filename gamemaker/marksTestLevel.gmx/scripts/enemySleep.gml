path_end();

self.state = "sleep";





if (sprite_index == imageLeft) {
    sprite_index = imageLeftSleep;
} else if (sprite_index == imageRight) {
    sprite_index = imageRightSleep;
} else if (sprite_index == imageFront) {
    sprite_index = imageFrontSleep;
} else if (sprite_index == imageTop) {
    sprite_index = imageTopSleep;
}

var sleepDuration = argument0;
alarm[0] = room_speed * sleepDuration;


