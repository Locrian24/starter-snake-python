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
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

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

class Board:
    def __init__(self):
        self.dimensions = (20, 20)
        self.food_list = []
        self.avoid = []

    def set_dimensions(self, width, height):
        self.dimensions = (width, height)

    def update(self, foods, enemies):
        del self.food_list[:]
        del self.avoid[:]

        for food in foods:
            self.food_list.append(Cell(food["x"], food["y"]))

        for enemy in enemies:
            for body in enemy["body"]:
                self.avoid.append(Cell(body["x"], body["y"]))

    def __get_closest_food(self, head, foods):
        if not foods:
            return None

        closest_food = foods[0]
        if len(foods) > 1:
            for food in foods[1:]:
                if head.man_distance(food) < head.man_distance(closest_food):
                    closest_food = food

        return closest_food


    def get_next_move(self, snake_head):
        food_available = self.food_list[:]
        head = Cell(snake_head["x"], snake_head["y"])
        closest_food = self.__get_closest_food(head, food_available)

        astar_path = self.astar(head, closest_food, self.avoid)
        while not astar_path:
            food_available.remove(closest_food)
            closest_food = self.__get_closest_food(head, food_available)
            astar_path = self.astar(head, closest_food, self.avoid)

        return astar_path

    def __get_lowest_f(self, cell_list):
        min_cell = cell_list[0]
        if len(cell_list) > 1:
            for cell in cell_list[1:]:
                if cell.f < min_cell.f:
                    min_cell = cell
        return min_cell

    def __reconstruct_path(self, current, start, return_list=None):
        if not return_list:
            return_list = []
        if not current.parent:
            return_list.append(current)
            return

        return_list.append(current)
        self.__reconstruct_path(current.parent, start, return_list)

        return return_list[::-1]

    def astar(self, start, end, avoid):
        #start by adding the original position to the open list
        open_list = [start]
        closed_list = []

        #hwile the open list is not empty
        while open_list:
            #get the square with the lowest F score
            current = self.__get_lowest_f(open_list)
            #add the current square to the closed list
            closed_list.append(current)
            #remove it fro the open list
            open_list.remove(current)
            #if we added the destination to the closed list, we've found a path
            if current == end:
                #break the loop
                return self.__reconstruct_path(current, start)
            #retrieve all its walkable neighbours
            #for all neighbours:
            for neighbour in current.get_neighbours(avoid, self.dimensions):
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
        
def main():
    board = {
    "food": [{"y": 12, "x": 9}, {"y": 5, "x": 2}, {"y": 13, "x": 7}, {"y": 0, "x": 10}, {"y": 13, "x": 6}, {"y": 14, "x": 7}, {"y": 9, "x": 4}, {"y": 4, "x": 10}, {"y": 3, "x": 13}, {"y": 14, "x": 4}],

    "width": 15,

    "snakes":
    [
    {"body": [{"y": 6, "x": 11}, {"y": 6, "x": 12}, {"y": 7, "x": 12}],
    "health": 98, "id": "71bc0613-00f6-4e6e-be72-4d84d19e568f",
    "name": ""}
    ],

    "height": 15
    }

    board_object = Board()
    board_object.set_dimensions(board["width"], board["height"])
    board_object.update(board["food"], board["snakes"])

    path = board_object.astar({"y": 2, "x": 3}, board_object.food_list[1], board_object.avoid)

    for p in path:
        print(p)

if __name__ == "__main__":
    main()