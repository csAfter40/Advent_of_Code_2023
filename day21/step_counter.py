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
        self.parser_class = parser_class

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def get_start(self):
        for j, row in enumerate(self.map):
            for i, char in enumerate(row):
                if char == "S":
                    return (j, i)
        raise ValueError("start point not found")

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.map = parser.setup_matrix()
        self.start = self.get_start()
        # print(self.start)
        self.map[self.start[0]][self.start[1]] = "."
        # MatrixParser.print_matrix(self.map)

    def get_valid_neighbors(self, pos):
        valid_neighbors = set()
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
        for dir in directions:
            try:
                if self.map[pos[0] + dir[0]][pos[1] + dir[1]] == ".":
                    valid_neighbors.add((pos[0] + dir[0], pos[1] + dir[1]))
            except IndexError:
                continue
        return valid_neighbors

    def get_destination_qty(self, steps):
        self.start = (0, 5)
        current_destinations = {self.start}
        for i in range(steps):
            next_destinations = set()
            for destination in current_destinations:
                valid_neighbors = self.get_valid_neighbors(destination)
                next_destinations = next_destinations.union(valid_neighbors)
            current_destinations = next_destinations
            print(len(current_destinations))
        return len(current_destinations)


if __name__ == "__main__":
    # input_file_path = "day21/test_input.txt"
    input_file_path = "day21/input.txt"
    # TOTAL_STEPS = 6
    TOTAL_STEPS = 64
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    print(app.get_destination_qty(TOTAL_STEPS))
