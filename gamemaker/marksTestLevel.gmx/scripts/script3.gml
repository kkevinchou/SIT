node = argument0

neighbours = ds_list_create()

        for x in range(-1, 2):
            for y in range(-1, 2):
                neighbour = [node[0] + x, node[1] + y]
                if (x != 0 or y != 0):
                    if (self._validNode(neighbour)):
                        neighbours.append(neighbour)

        return neighbours
