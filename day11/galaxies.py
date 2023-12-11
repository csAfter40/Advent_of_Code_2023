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
        self.parser_class = parser_class
        self.galaxies = []

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.data = parser.setup_matrix()
        self.set_enlarged_universe()
        self.set_galaxies()

    def get_empty_rows(self):
        empty_rows = []
        for i, row in enumerate(self.data):
            if all([item == "." for item in row]):
                empty_rows.append(i)
        return empty_rows

    def get_empty_cols(self):
        empty_cols = []
        for i in range(len(self.data)):
            col = [row[i] for row in self.data]
            if all(item == "." for item in col):
                empty_cols.append(i)
        return empty_cols

    def set_enlarged_universe(self):
        universe = copy.deepcopy(self.data)
        empty_rows = self.get_empty_rows()
        empty_cols = self.get_empty_cols()
        for row_number in reversed(empty_rows):
            universe.insert(row_number, universe[row_number].copy())
        for row in universe:
            for col_number in reversed(empty_cols):
                row.insert(col_number, ".")
        self.universe = universe

    def set_galaxies(self):
        for j, row in enumerate(self.universe):
            for i, item in enumerate(row):
                if item == "#":
                    self.galaxies.append((j, i))

    def get_manhattan_distance(self, galaxy1, galaxy2):
        return abs(galaxy2[0] - galaxy1[0]) + abs(galaxy2[1] - galaxy1[1])

    def get_total_distance(self):
        distances = []
        for i, galaxy in enumerate(self.galaxies[:-1]):
            for other_galaxy in self.galaxies[i + 1 :]:
                distances.append(self.get_manhattan_distance(galaxy, other_galaxy))
        return sum(distances)


if __name__ == "__main__":
    input_file_path = "day11/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    print(app.get_total_distance())
