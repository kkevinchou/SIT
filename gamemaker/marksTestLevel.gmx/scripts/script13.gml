
var myX = argument0
var myY = argument1
var otherX = argument2
var otherY = argument3
var object = argument4


blockers = ds_priority_create();
with (all) {
  if (collision_line(myX, myY, otherX, otherX, object, false, false)) {
    ds_priority_add(other.blockers, id, point_distance(x, y, other.x, other.y));
  }
}

blocking_object = collision_line(myX, myY, otherX, otherY, object, false, false)
while (blocking_object) {
    old_blocking = blocking_object
    blocking_object = collision_line(myX, myY, blocking_object.x, blocking_object.y, object, false, false)
}
return old_blocking
