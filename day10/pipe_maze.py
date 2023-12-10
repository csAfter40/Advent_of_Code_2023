class MatrixParser:
    def __init__(self, lines):
        self.lines = lines
        self.matrix = self.setup_matrix()

    def setup_matrix(self):
        matrix = []
        for line in self.lines:
            matrix_line = []
            for char in line:
                matrix_line.append(char)
            matrix.append(matrix_line)
        return matrix

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            print(*row, sep="")


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.lines = []
        self.parser_class = parser_class
        self.route = []
        self.movement_map = {
            "|": ((-1, 0), (1, 0)),
            "-": ((0, -1), (0, 1)),
            "L": ((0, 1), (-1, 0)),
            "J": ((-1, 0), (0, -1)),
            "7": ((0, -1), (1, 0)),
            "F": ((0, 1), (1, 0)),
        }
        self.inside_tile_set = set()

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def get_start_point(self):
        for j, row in enumerate(self.data):
            for i, char in enumerate(row):
                if char == "S":
                    return (j, i)

    def get_char(self, location):
        return self.data[location[0]][location[1]]

    def get_start_point_shape(self):
        movement_directions = []
        # check right
        if self.start_point[1] < len(self.data[0]) - 1:
            if (0, -1) in self.movement_map[
                self.data[self.start_point[0]][self.start_point[1] + 1]
            ]:
                movement_directions.append((0, 1))
        # check left
        if self.start_point[1] > 0:
            if (0, 1) in self.movement_map[
                self.data[self.start_point[0]][self.start_point[1] - 1]
            ]:
                movement_directions.append((0, -1))
        # check down
        if self.start_point[0] < len(self.data) - 1:
            if (-1, 0) in self.movement_map[
                self.data[self.start_point[0] + 1][self.start_point[1]]
            ]:
                movement_directions.append((1, 0))
        # check up
        if self.start_point[0] > 0:
            if (1, 0) in self.movement_map[
                self.data[self.start_point[0] - 1][self.start_point[1]]
            ]:
                movement_directions.append((-1, 0))
        for char, values in self.movement_map.items():
            if movement_directions[0] in values and movement_directions[1] in values:
                return char

    def setup_data(self):
        for line in self.get_lines():
            self.lines.append(line)
        parser = self.parser_class(self.lines)
        self.data = parser.matrix
        self.start_point = self.get_start_point()
        self.start_point_shape = self.get_start_point_shape()
        self.start_loop()
        self.route_set = set(self.route)
        self.set_enclosed_tiles()

    def get_inverted_direction(self, direction):
        return (direction[0] * -1, direction[1] * -1)

    def get_next_direction(self, previous_direction, char):
        inverted_direction = self.get_inverted_direction(previous_direction)
        if inverted_direction == self.movement_map[char][0]:
            return self.movement_map[char][1]
        elif inverted_direction == self.movement_map[char][1]:
            return self.movement_map[char][0]
        else:
            raise ValueError

    def get_next_position(self, current, direction):
        return (current[0] + direction[0], current[1] + direction[1])

    # def make_a_loop(self, direction, next):
    #     """
    #     this solution leads to a maximum recursion depth error
    #     """
    #     self.route.append(next)
    #     if self.data[next[0]][next[1]] == "S":
    #         return
    #     char = self.data[next[0]][next[1]]
    #     next_direction = self.get_next_direction(direction, char)
    #     next_position = self.get_next_position(next, next_direction)
    #     # breakpoint()
    #     self.make_a_loop(next_direction, next_position)

    # def start_loop(self):
    #     current = self.start_point
    #     direction = self.initial_direction
    #     next = self.get_next_position(current, direction)
    #     self.make_a_loop(direction, next)

    def start_loop(self):
        current = self.start_point
        direction = self.movement_map[self.start_point_shape][0]
        next = self.get_next_position(current, direction)
        while True:
            self.route.append(next)
            if self.data[next[0]][next[1]] == "S":
                return
            char = self.data[next[0]][next[1]]
            next_direction = self.get_next_direction(direction, char)
            next_position = self.get_next_position(next, next_direction)
            direction = next_direction
            next = next_position

    def calculate_furthest_distance(self):
        return int(len(self.route) / 2)

    # --------------Part2-----------------------
    def get_starting_tiles(self):
        for j, row in enumerate(self.data):
            for i, char in enumerate(row):
                if (j, i) in self.route_set:
                    assert char == "F"
                    return (j + 1, i + 1), (j, i)

    def get_inside_neighbors(self, current_tile, previous_tile):
        """
        We start from the top left route tile, which is always an "F", and go to right direction.
        """
        inside_neighbor_map = {
            "|": {(1, 0): ((0, 1),), (-1, 0): ((0, -1),)},
            "-": {(0, -1): ((1, 0),), (0, 1): ((-1, 0),)},
            "L": {(-1, 0): ((0, -1), (1, -1), (1, 0)), (0, 1): ((-1, 1),)},
            "J": {(-1, 0): ((-1, -1),), (0, -1): ((1, 0), (1, 1), (0, 1))},
            "7": {(1, 0): ((0, 1), (-1, 1), (-1, 0)), (0, -1): ((1, -1),)},
            "F": {(1, 0): ((1, 1),), (0, 1): ((-1, 0), (-1, -1), (0, -1))},
        }
        direction = (
            previous_tile[0] - current_tile[0],
            previous_tile[1] - current_tile[1],
        )
        current_char = self.get_char(current_tile)
        current_neighbors = []
        for neighbor in inside_neighbor_map[current_char][direction]:
            current_neighbors.append(
                (current_tile[0] + neighbor[0], current_tile[1] + neighbor[1])
            )
        return current_neighbors

    def set_route_direction(self, tile):
        tile_index = self.route.index(tile)
        try:
            next_tile = self.route[tile_index + 1]
        except IndexError:
            next_tile = self.route[0]
        if next_tile[1] == tile[1]:
            return self.route.reverse()

    def add_tile_to_insides(self, tile):
        self.inside_tile_set.add(tile)
        neighbors = []
        # check right
        if tile[1] < len(self.data[0]) - 1:
            neighbors.append(((tile[0]), tile[1] + 1))
        # check left
        if tile[1] > 0:
            neighbors.append(((tile[0]), tile[1] - 1))
        # check down
        if tile[0] < len(self.data) - 1:
            neighbors.append(((tile[0] + 1), tile[1]))
        # check up
        if tile[0] > 0:
            neighbors.append(((tile[0] - 1), tile[1]))
        for neighbor in neighbors:
            if neighbor not in self.route_set and neighbor not in self.inside_tile_set:
                self.add_tile_to_insides(neighbor)

    def set_starting_point_shape(self):
        char = self.get_start_point_shape()
        self.data[self.start_point[0]][self.start_point[1]] = char

    def set_enclosed_tiles(self):
        # find a route node close to matrix edges and decide which side is inside
        # loop through the route and check inside neighbors
        # if a neighbor tile is not a route tile, than it is an inside tile
        # check neighbors of this inside tile if there is are adjacent inside tiles and do this step recursively
        inside_neighbor, route_tile = self.get_starting_tiles()
        self.set_starting_point_shape()
        self.set_route_direction(route_tile)
        current_index = self.route.index(route_tile)
        current_neighbors = [inside_neighbor]
        for _ in range(len(self.route)):
            for neighbor in current_neighbors:
                if (
                    neighbor not in self.route_set
                    and neighbor not in self.inside_tile_set
                ):
                    self.add_tile_to_insides(neighbor)
            next_index = (current_index + 1) % len(self.route)
            current_neighbors = self.get_inside_neighbors(
                current_tile=self.route[next_index],
                previous_tile=self.route[current_index],
            )
            current_index = next_index

    def get_enclosed_tiles_qty(self):
        return len(self.inside_tile_set)


if __name__ == "__main__":
    input_file_path = "day10/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    # part 1
    print(app.calculate_furthest_distance())
    # part 2
    print(app.get_enclosed_tiles_qty())
