var myX = argument0
var myY = argument1
var otherX = argument2
var otherY = argument3
var object = argument4


var old_blocking = noone
var rot = degtorad( point_direction(myX,myY,otherX,otherY) +90)
var blocking_object = collision_line(myX, myY, otherX, otherY, object, false, true)
while (blocking_object) {
    
    var dist = distance_to_object(blocking_object)
    dist = max(0,dist-16)
    var newX = myX + sin(rot) * dist
    var newY = myY + cos(rot) * dist

    if (old_blocking == blocking_object) break;
    
    old_blocking = blocking_object
    if (dist==0) break;
    blocking_object = collision_line(myX, myY, newX, newY, object, false, true)
}

return old_blocking












