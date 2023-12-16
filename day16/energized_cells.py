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

    def print_matrix(matrix):
        for row in matrix:
            print(*row, sep="")


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.data = []
        self.parser_class = parser_class
        self.energized_cells = set()

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.map = parser.setup_matrix()

    def is_valid_cell(self, cell):
        if 0 <= cell[0] < len(self.map) and 0 <= cell[1] < len(self.map[0]):
            return True
        return False

    def get_movement(self, char, direction):
        assert char in ".-|/\\"
        if char == ".":
            return (direction,)
        if char == "-":
            if direction[0] == 0:
                return (direction,)
            else:
                return ((0, 1), (0, -1))
        if char == "|":
            if direction[1] == 0:
                return (direction,)
            else:
                return ((1, 0), (-1, 0))
        if char == "/":
            return ((-1 * direction[1], -1 * direction[0]),)
        if char == "\\":
            return ((direction[1], direction[0]),)

    def get_next_cells(self, cell, direction):
        cell_direction_couples = []
        char = self.map[cell[0]][cell[1]]
        movements = self.get_movement(char, direction)
        for movement in movements:
            next_cell = (cell[0] + movement[0], cell[1] + movement[1])
            next_direction = movement
            cell_direction_couples.append((next_cell, next_direction))
        return cell_direction_couples

    def run_light(self, cell, direction, energized_cells):
        cell = cell
        direction = direction
        while True:
            if (cell, direction) in energized_cells:
                break
            energized_cells.add((cell, direction))
            next_cells = self.get_next_cells(cell, direction)
            if len(next_cells) == 2:
                next_cell, next_direction = next_cells[1]
                if self.is_valid_cell(next_cell):
                    self.run_light(next_cell, next_direction, energized_cells)
            cell, direction = next_cells[0]
            if not self.is_valid_cell(cell):
                break

    def get_energized_cell_qty(self, init_cell, init_direction):
        energized_cells = set()
        self.run_light(init_cell, init_direction, energized_cells)
        return len(set([cell[0] for cell in energized_cells]))

    def get_initial_movements(self):
        initial_movements = []
        # from left to right
        initial_movements.extend([((i, 0), (0, 1)) for i in range(len(self.map))])
        # from right to left
        initial_movements.extend(
            [((i, len(self.map[0]) - 1), (0, -1)) for i in range(len(self.map))]
        )
        # from top to bottom
        initial_movements.extend([((0, i), (1, 0)) for i in range(len(self.map[0]))])
        # from bottom to top
        initial_movements.extend(
            [((len(self.map) - 1, i), (-1, 0)) for i in range(len(self.map[0]))]
        )
        return initial_movements

    def get_max_energized_cell_qty(self):
        energized_cell_qtys = []
        initial_movements = self.get_initial_movements()
        for initial_movement in initial_movements:
            energized_cell_qtys.append(
                self.get_energized_cell_qty(initial_movement[0], initial_movement[1])
            )
        return max(energized_cell_qtys)


if __name__ == "__main__":
    # input_file_path = "day16/test_input.txt"
    input_file_path = "day16/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    # Part 1
    print(app.get_energized_cell_qty(init_cell=(0, 0), init_direction=(0, 1)))
    # Part 2
    print(app.get_max_energized_cell_qty())
