var grid = argument0
var node = argument1

var neighbours = ds_list_create()

for (var i = -1; i < 2; i++) {
    for (var j = -1; j < 2; j++) {
        var neighbour = createNode(getX(node) + i, getY(node) + j)
        if (i == 0 && j == 0) {
            continue
        }
        if (nodeIsOkay(grid, neighbour)) {
            ds_list_add(neighbours, neighbour)
        }
    }
}

return neighbours
