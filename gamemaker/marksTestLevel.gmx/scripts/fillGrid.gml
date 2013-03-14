grid = argument0
startNode = argument1

open_list = ds_list_create()
closed_list = ds_list_create()

ds_list_add(open_list, node)

resetGrid(grid)

while (ds_list_size(open_list) > 0) {
    node = ds_list_find_value(open_list, 0)
    ds_list_add(closed_list, node)
    ds_list_delete(open_list, 0)
    
    
}
