DIMENSIONS = (5, 5)

class Cell:
    def __init__(self, x, y, parent=None):
        self.x, self.y = x, y
        self.parent = parent

        self.g = 0
        self.h = 0
        self.f = 0

    def __repr__(self):
        return "[{}, {}]".format(self.x, self.y)

    def __eq__(self, other):
        if not other:
            print("ERROR")
            return False

        return self.x == other.x and self.y == other.y

    def man_distance(self, goal):
        return abs(self.x - goal.x) + abs(self.y - goal.y)

    def eu_distance(self, goal):
        return ( (self.x - goal.x)**2 + (self.y - goal.y)**2 )**0.5

    def get_neighbours(self, avoid, dimensions):
        neighbour_list = []
        for next_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            current_cell = Cell(self.x + next_coord[0], self.y + next_coord[1], self)
            if  current_cell.x < 0 or current_cell.x > dimensions[0] - 1 or \
                current_cell.y < 0 or current_cell.y > dimensions[1] - 1 or \
                current_cell in avoid:  #not walkable
                continue

            neighbour_list.append(current_cell)
        return neighbour_list
    
def get_lowest_f(cell_list):
    min_cell = cell_list[0]
    if len(cell_list) > 1:
        for cell in cell_list:
            if cell.f < min_cell.f:
                min_cell = cell
    return min_cell

def reconstruct_path(current, start, return_list=None):
    if not return_list:
        return_list = []
    if not current.parent:
        return_list.append(current)
        return

    return_list.append(current)
    reconstruct_path(current.parent, start, return_list)

    return return_list[::-1]

def astar(start, end, avoid, dimensions):
    #start by adding the original position to the open list
    open_list = [start]
    closed_list = []

    #hwile the open list is not empty
    while open_list:
        #get the square with the lowest F score
        current = get_lowest_f(open_list)
        #add the current square to the closed list
        closed_list.append(current)
        #remove it fro the open list
        open_list.remove(current)
        #if we added the destination to the closed list, we've found a path
        if not end:
            print("HELP")

        if current == end:
            #break the loop
            return reconstruct_path(current, start)
        #retrieve all its walkable neighbours
        #for all neighbours:
        for neighbour in current.get_neighbours(avoid, dimensions):
            #if the neighbour is already in the closed list, skip it
            if neighbour in closed_list:
                continue

            temp_g = current.g + 1

            #if it's not in the open list
            if neighbour not in open_list:
                open_list.append(neighbour)
                

                #compute its score and set the parent
                # (done in neighbour comparison)
            #else
            else:
                #test if calculating F from the current path is lower than the
                #already calculated F score at that point
                stored_g = open_list[open_list.index(neighbour)].g
                if temp_g >= stored_g:
                    continue
            
            neighbour.g = current.g + 1
            neighbour.h = neighbour.eu_distance(end)
            neighbour.f = neighbour.g + neighbour.h
    
    def flood_fill(self, current, num_safe, max_len, visited, avoid):
        """
            Determine available spaces as well as shutting off any
            cells with one walkable neighbour (unvisited), effectively
            blocking off dead ends
        """
        if not visited:
            visited = []

        if num_safe >= max_len:
            return num_safe

        if current not in visited:
            visited.append(current)
            num_safe += 1
            n = len(current.get_neighbours(avoid)
            for n in current.get_neighbours(avoid)
        
        