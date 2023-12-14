import copy


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

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        for line in self.get_lines():
            self.lines.append(line)
        parser = self.parser_class(self.lines)
        self.platform = parser.matrix

    def get_next_position(self, initial_position, platform):
        next_position = initial_position
        j, i = next_position
        while True:
            if j == 0:
                break
            if platform[j - 1][i] == ".":
                next_position = (j - 1, i)
                j, i = next_position
                continue
            else:
                break
        return next_position

    def tilt_platform(self, platform):
        tilted_platform = copy.deepcopy(platform)
        for j, row in enumerate(platform):
            for i, char in enumerate(row):
                if char == "O":
                    next_position = self.get_next_position((j, i), tilted_platform)
                    tilted_platform[next_position[0]][i], tilted_platform[j][i] = (
                        tilted_platform[j][i],
                        tilted_platform[next_position[0]][i],
                    )
        return tilted_platform

    def calculate_load(self, platform):
        load = 0
        for j, row in enumerate(platform):
            for char in row:
                if char == "O":
                    magnitude = len(platform) - j
                    load += magnitude
        return load

    def rotate_platform(self, platform, direction):
        assert direction in "NESW"
        if direction == "N":
            rotated_platform = platform
        if direction == "W":
            # rotate clockwise
            rotated_platform = [list(reversed(col)) for col in zip(*platform)]
        if direction == "E":
            # rotate counter-clockwise
            rotated_platform = list(reversed([list(col) for col in zip(*platform)]))
        if direction == "S":
            # rotate 180 degs
            rotated_platform = list(reversed([list(reversed(col)) for col in platform]))

        return rotated_platform

    def rotate_platform_backward(self, platform, direction):
        assert direction in "NESW"
        if direction == "N":
            rotated_platform = platform
        if direction == "S":
            rotated_platform = self.rotate_platform(platform, "S")
        if direction == "E":
            rotated_platform = self.rotate_platform(platform, "W")
        if direction == "W":
            rotated_platform = self.rotate_platform(platform, "E")
        return rotated_platform

    def make_cycle(self, platform):
        directions = ["N", "W", "S", "E"]
        moving_platform = copy.deepcopy(platform)
        for direction in directions:
            rotated_platform = self.rotate_platform(moving_platform, direction)
            tilted_platform = self.tilt_platform(rotated_platform)
            moving_platform = self.rotate_platform_backward(tilted_platform, direction)
        return moving_platform

    def find_pattern(self):
        cycles = [self.platform]
        previous_cycle = self.platform
        cycle = 0
        while True:
            next_cycle = self.make_cycle(previous_cycle)
            if next_cycle in cycles:
                break
            previous_cycle = next_cycle
            cycles.append(next_cycle)
            cycle += 1
        return cycles.index(next_cycle), cycle + 1

    def get_platform_after_cycles(self, qty):
        previous_cycle = self.platform
        for i in range(qty):
            next_cycle = self.make_cycle(previous_cycle)
            previous_cycle = next_cycle
        return next_cycle

    def calculate_load_in_direction(self, direction):
        rotated_platform = self.rotate_platform(self.platform, direction)
        tilted_platform = self.tilt_platform(rotated_platform)
        return self.calculate_load(tilted_platform)

    def get_load_after_cycles(self, qty):
        index_1, index_2 = self.find_pattern()
        final_index = (qty - index_1) % (index_2 - index_1) + index_1
        final_platform = self.get_platform_after_cycles(final_index)
        return self.calculate_load(final_platform)


if __name__ == "__main__":
    # input_file_path = "day14/test_input.txt"
    input_file_path = "day14/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    # part 1
    print(app.calculate_load_in_direction("N"))
    # part 2
    print(app.get_load_after_cycles(1000000000))
