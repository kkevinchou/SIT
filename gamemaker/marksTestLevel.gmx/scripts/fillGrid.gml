var grid = argument0
var goal = argument1

resetGrid(grid)

var open_list = ds_list_create()
var closed_list = ds_list_create()

ds_grid_set(grid, getX(goal), getY(goal), 0)
ds_list_add(open_list, goal)

while (ds_list_size(open_list) > 0) {
    var parent = pop_front(open_list)
    ds_list_add(closed_list, parent)
    
    var parentDist = getNodeValFromGrid(grid, parent)
    var neighbours = getNeighbours(grid, parent)
    
    while (ds_list_size(neighbours) > 0) {
        var neighbour = pop_front(neighbours)
        
        var dist = parentDist
        if (getX(neighbour) == getX(parent) || getY(neighbour) == getY(parent)) {
            dist += 1
        } else {
            dist += 1.4
        }
        
        if (abs(getX(neighbour) - getX(goal)) > 10 || abs(getY(neighbour) - getY(goal)) > 10) {
            continue
        }
        
        if (dist < getNodeValFromGrid(grid, neighbour)) {
            ds_grid_set(grid, getX(neighbour), getY(neighbour), dist)
        }
        
        if (!listHasNode(open_list, neighbour) && !listHasNode(closed_list, neighbour)) {
            ds_list_add(open_list, neighbour)
        }
    }
    
    //ds_list_destroy(neighbours)
}

//while (ds_list_size(open_list) > 0) {
//    var node = pop_front(open_list)
//    ds_list_destroy(node)
//}
//ds_list_destroy(open_list)
