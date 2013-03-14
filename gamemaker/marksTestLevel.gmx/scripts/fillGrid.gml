grid = argument0
goal_x = argument1
goal_y = argument2

goal[0] = goal_x
goal[1] = goal_y

resetGrid(grid)
open_list = ds_list_create()
closed_list = ds_list_create()

ds_grid_set(grid, goal[0], goal[1], 0)
ds_list_add(open_list, node)

while (ds_list_size(open_list) > 0) {
    parent = ds_list_find_value(open_list, 0)
    
    ds_list_add(closed_list, parent)
    ds_list_delete(open_list, 0)
    
    parentDist = ds_grid_get(grid, parent[0], parent[1])
    neighbours = getNeighbours(grid, parent[0], parent[1])
    
    while (ds_list_size(neighbours) > 0) {
        neighbour = ds_list_find_value(neighbours, 0)
        ds_list_delete(neighbours, 0)
        
        dist = parentDist
        if (neighbour[0] == parent[0] || neighbour[1] == parent[1]) {
            dist++
        } else {
            dist += 1.4
        }
        
        if (dist < ds_grid_get(grid, neighbour[0], neighbour[1])) {
            ds_grid_set(grid, neighbour[0], neighbour[1], dist)
            ds_list_add(open_list, neighbour)
        }
    }
}

/*
    while len(self.open) > 0:
        n = self.open[0]
        parentDist = self.mapdata[n[0]][n[1]]
        neighbours = self._getNeighbours(n)
        for neighbour in neighbours:
            # if diagonal, cost is 1.4.
            # if axis aligned, cost is 1
            dist = parentDist + 1 if (neighbour[0] == n[0] or neighbour[1] == n[1]) else parentDist + 1.4
            if (dist < self.mapdata[neighbour[0]][neighbour[1]]):
                self.mapdata[neighbour[0]][neighbour[1]] = dist
                self.open.append(neighbour)
        self.open.remove(n)
*/
