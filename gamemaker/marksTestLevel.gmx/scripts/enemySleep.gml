path_end();

self.state = "sleep";

if (sprite_index == bodygaurdLeft) {
    sprite_index = securityGuardSleepLeft;
} else if (sprite_index == bodygaurdRight) {
    sprite_index = securityGuardSleepRight;
} else if (sprite_index == bodygaurdFront) {
    sprite_index = securityGuardSleepFront;
} else if (sprite_index == bodygaurdTop) {
    sprite_index = securityGuardSleepBack;
}

var sleepDuration = argument0;
alarm[0] = room_speed * sleepDuration;
