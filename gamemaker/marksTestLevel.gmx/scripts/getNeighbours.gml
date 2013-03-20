var grid = argument0
var node = argument1

var neighbours = ds_list_create()


// Diagonal neighbours

/*
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
*/

var neighbourRight = createNode(getX(node) + 1, getY(node) + 0)
if (nodeIsOkay(grid, neighbourRight)) {
    ds_list_add(neighbours, neighbourRight)
}

var neighbourLeft = createNode(getX(node) - 1, getY(node) + 0)
if (nodeIsOkay(grid, neighbourLeft)) {
    ds_list_add(neighbours, neighbourLeft)
}

var neighbourUp = createNode(getX(node) + 0, getY(node) + 1)
if (nodeIsOkay(grid, neighbourUp)) {
    ds_list_add(neighbours, neighbourUp)
}

var neighbourDown = createNode(getX(node) + 0, getY(node) - 1)
if (nodeIsOkay(grid, neighbourDown)) {
    ds_list_add(neighbours, neighbourDown)
}

return neighbours
