var grid = argument0
var node = argument1

if (getX(node) >= 0 && getY(node) >= 0) {
    if (getX(node) < ds_grid_width(grid) && getY(node) < ds_grid_height(grid)) {
        if (ds_grid_get(grid, getX(node), getY(node)) >= 0) {
            return true
        }
    }
}

return false
            
