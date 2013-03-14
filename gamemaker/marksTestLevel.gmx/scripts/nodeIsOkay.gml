grid = argument0
node_x = argument1
node_y = argument2

node[0] = node_x
node[1] = node_y

return (node[0] >= 0 && node[1] >= 0 &&
            node[0] < ds_grid_width(grid) && node[1] < ds_grid_height(grid) &&
            ds_grid_get(grid, node[0], node[1]) >= 0)
