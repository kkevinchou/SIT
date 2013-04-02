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
    }
}

var chatObj = instance_create(x, y, obj_nemesis_chat);
chatObj.dartHit = dartHit;
