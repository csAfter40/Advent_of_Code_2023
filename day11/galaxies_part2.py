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
    def __init__(self, file_path, parser_class, expansion_ratio):
        self.file_path = file_path
        self.parser_class = parser_class
        self.galaxies = []
        self.expansion_ratio = expansion_ratio

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.universe = parser.setup_matrix()
        self.set_galaxies()
        self.expansion_matrix = self.set_expansion_matrix()
        self.apply_expansion()
        # MatrixParser.print_matrix(self.expansion_matrix)

    def set_expansion_matrix(self):
        return [[[1, 1] for item in row] for row in self.universe]

    def get_empty_rows(self):
        empty_rows = []
        for i, row in enumerate(self.universe):
            if all([item == "." for item in row]):
                empty_rows.append(i)
        return empty_rows

    def get_empty_cols(self):
        empty_cols = []
        for i in range(len(self.universe)):
            col = [row[i] for row in self.universe]
            if all(item == "." for item in col):
                empty_cols.append(i)
        return empty_cols

    def apply_expansion(self):
        empty_rows = self.get_empty_rows()
        empty_cols = self.get_empty_cols()
        for row in empty_rows:
            for item in self.expansion_matrix[row]:
                item[0] *= self.expansion_ratio
        for col in empty_cols:
            for row in self.expansion_matrix:
                row[col][1] *= self.expansion_ratio

    def set_galaxies(self):
        for j, row in enumerate(self.universe):
            for i, item in enumerate(row):
                if item == "#":
                    self.galaxies.append((j, i))

    def get_horizontal_distance(self, galaxy1, galaxy2):
        horizontal_distance = 0
        dist_x = galaxy2[1] - galaxy1[1]
        if dist_x == 0:
            return 0
        dir_x = int(dist_x / abs(dist_x))
        for i in range(0, dist_x, dir_x):
            horizontal_distance += self.expansion_matrix[galaxy1[0]][
                galaxy1[1] + i + dir_x
            ][1]
        return horizontal_distance

    def get_vertical_distance(self, galaxy1, galaxy2):
        vertical_distance = 0
        dist_y = galaxy2[0] - galaxy1[0]
        if dist_y == 0:
            return 0
        dir_y = int(dist_y / abs(dist_y))
        for i in range(0, dist_y, dir_y):
            vertical_distance += self.expansion_matrix[galaxy1[0] + i + dir_y][
                galaxy1[1]
            ][0]
        return vertical_distance

    def get_galaxy_distance(self, galaxy1, galaxy2):
        horizontal_distance = self.get_horizontal_distance(galaxy1, galaxy2)
        vertical_distance = self.get_vertical_distance(galaxy1, galaxy2)
        return horizontal_distance + vertical_distance

    def get_total_distance(self):
        distances = []
        for i, galaxy in enumerate(self.galaxies[:-1]):
            for other_galaxy in self.galaxies[i + 1 :]:
                distances.append(self.get_galaxy_distance(galaxy, other_galaxy))
        return sum(distances)


if __name__ == "__main__":
    expansion_ratio = 1000000
    input_file_path = "day11/input.txt"
    app = App(input_file_path, MatrixParser, expansion_ratio)
    app.setup_data()
    print(app.get_total_distance())
