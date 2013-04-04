var chatObj = instance_nearest(x, y, obj_nemesis_chat);
if (chatObj) {
    with (chatObj) {
        instance_destroy();
    }
}

var dartHit = false;
if (state == "chase") {
} else {
    dartHit = true;
    self.numDartHits++;
    if (numDartHits >= 3) {
        self.state = "sleep";
        cutscene_manager.current_room = 4
        cutscene_manager.next_room = 4
        room_goto(cutscreen)

    }
}

var dartObj = instance_nearest(x, y, sleepDart);
self.state = "investigate";
self.investigateTargetX = dartObj.startX;
self.investigateTargetY = dartObj.startY;

var chatObj = instance_create(x, y, obj_nemesis_chat);
chatObj.dartHit = dartHit;
