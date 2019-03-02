from board import Board
from constants import Constants

class Snake:
    def __init__(self, board_reference):
        self.body = []
        self.length = 3
        self.health = -1
        self.state = "grow"

        self.__board = board_reference

    def update(self, body, health, state="grow"):
        """ Keeps snake info updated every loop. Currently, body stores positional dictionary """

        self.body = body
        self.length = len(self.body)
        self.health = health
        self.state = state

    def move(self):
        """
            This method is what is called every game loop and will determine the next move
            Based off of the current state, suitable methods will be called and analysed to \
                determine the best path possible
        """
        

        next_path = self.__board.get_next_move(self, 0)
        # next_area = self.__board.count_connected_comps(next_path[1])

        if not next_path:
            next_path = self.__board.get_next_move(self, 7)
        next_move = next_path[1] - next_path[0]
        # if next_area < self.length:
        #     next_move = (-next_move[0], -next_move[1])

        # if self.__board.is_position_in(next_move, self.__board.avoid):
        #     print("TIME TO DIE")
        next_vector = Constants.VECTORS[next_move]

        return next_vector

    def change_state(self, new_state):
        self.state = new_state

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[1:]

    def get_tailend(self):
        return self.body[-1]

    def get_health(self):
        return self.health

def main():
    data = {

    "turn": 2,
    "game": {
    "id": "d58d8f06-9f3e-48c6-a825-6f4d7e9b5c4e"
    },

    "board": {
    "food": [{"y": 12, "x": 9}, {"y": 5, "x": 2}, {"y": 13, "x": 7}, {"y": 0, "x": 10}, {"y": 13, "x": 6}, {"y": 14, "x": 7}, {"y": 9, "x": 4}, {"y": 4, "x": 10}, {"y": 3, "x": 13}, {"y": 14, "x": 4}],

    "width": 15,

    "snakes":
    [
    {"body": [{"y": 6, "x": 11}, {"y": 6, "x": 12}, {"y": 7, "x": 12}],
    "health": 98, "id": "71bc0613-00f6-4e6e-be72-4d84d19e568f",
    "name": ""}
    ],

    "height": 15
    },

    "you": {

    "body": [{"y": 5, "x":8}, {"y": 5, "x": 7}, {"y": 5, "x": 9}],
    "health": 98, "id": "a27a9953-76cb-4307-a198-bd4d5043218a",
    "name": ""

    }

    }

    bord = Board()
    bord.set_dimensions(data["board"]["width"], data["board"]["height"])
    bord.update(data["board"]["food"], data["board"]["snakes"])

    snek = Snake(bord)
    snek.update(data["you"]["body"], data["you"]["health"])

    snek.move()


if __name__ == "__main__":
    main()