grid = argument0
node = argument1

neighbours = ds_list_create()

for (x = -1; x < 2; x++) {
    for (y = -1; y < 2; y++) {
        neighbour[0] = node[0] + x
        neighbour[1] = node[1] + y
        if (x == 0 && y == 0) {
            continue
        }
        if (nodeIsOkay(grid, neighbour[0], neighbour[1])) {
            ds_list_add(neighbours, neighbour)
        }
    }
}

return neighbours
