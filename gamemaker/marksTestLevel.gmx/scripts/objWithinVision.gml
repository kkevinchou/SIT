var targetObj = argument0;

if (!targetObj) {
    return false;
}

var directionToFlynn = point_direction(self.x,self.y,targetObj.x,targetObj.y);
var relativeDirection = directionToFlynn - direction;

if (relativeDirection < 0) {
    relativeDirection += 360;
}

var rangeOkay = false;

rangeMin = -(visionWidth / 2);
rangeMax = (visionWidth / 2);

if (relativeDirection <= rangeMax && relativeDirection >= rangeMin) {
    rangeOkay = true;
}

if (!rangeOkay) {
    rangeMin = -(visionWidth / 2) + 360;
    rangeMax = (visionWidth / 2) + 360;
    
    if (relativeDirection <= rangeMax && relativeDirection >= rangeMin) {
        rangeOkay = true;
    }
}

return rangeOkay;
