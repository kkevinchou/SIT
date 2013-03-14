grid = argument0

for (x = 0; x < ds_grid_width(grid); x++) {
    for (y = 0; y < ds_grid_height(grid); y++) {
        if (ds_grid_get(grid, x, y) != -1) {
            ds_grid_set(grid, x, y, global.pathMaxCost)
        }
    }
}
