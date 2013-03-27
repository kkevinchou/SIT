var myX = argument0
var myY = argument1
var otherX = argument2
var otherY = argument3
var object = argument4


old_blocking = noone
rot = degtorad( point_direction(myX,myY,otherX,otherY) +90)
blocking_object = collision_line(myX, myY, otherX, otherY, object, false, true)
while (blocking_object) {
    
    dist = distance_to_object(blocking_object)
    dist = max(0,dist-32)
    newX = myX + sin(rot) * dist
    newY = myY + cos(rot) * dist

    old_blocking = blocking_object
    if (dist==0) break;
    blocking_object = collision_line(myX, myY, newX, newY, object, false, true)

}

return old_blocking












