var grid = argument0

for (var i = 0; i < ds_grid_width(grid); i++) {
    for (var j = 0; j < ds_grid_height(grid); j++) {
        if (ds_grid_get(grid, i, j) != -1) {
            ds_grid_set(grid, i, j, global.pathMaxCost)
        }
    }
}
