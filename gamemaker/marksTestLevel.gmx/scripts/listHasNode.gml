var list = argument0
var node = argument1

for (var i = 0; i < ds_list_size(list); i++) {
    var g = ds_list_find_value(list, i)
    if (getX(g) == getX(node) && getY(g) == getY(node)) {
        return true
    }
}

return false
