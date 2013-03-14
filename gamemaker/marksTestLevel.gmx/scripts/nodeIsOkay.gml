grid = argument0
node = argument1

return (node[0] >= 0 && node[1] >= 0 && node[0] < ds_grid_width(grid) && node[1] < ds_grid_height(grid))
