import sys

sys.setrecursionlimit(10000)


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

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.map = parser.setup_matrix()
        self.finish = (len(self.map) - 1, len(self.map[0]) - 2)
        self.map[0][1] = "S"
        MatrixParser.print_matrix(self.map)

    def get_available_neighbors(self, path):
        pos = path[-1]
        available_neighbors = []
        if self.map[pos[0]][pos[1]] == ">":
            return [(pos[0], pos[1] + 1)]
        if self.map[pos[0]][pos[1]] == "v":
            return [(pos[0] + 1, pos[1])]
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
        for dir in directions:
            neighbor = (pos[0] + dir[0], pos[1] + dir[1])
            char = self.map[neighbor[0]][neighbor[1]]
            if char in ".>v" and neighbor not in path:
                if dir == (0, -1) and char == ">":
                    continue
                if dir == (-1, 0) and char == "v":
                    continue
                available_neighbors.append(neighbor)

        return available_neighbors

    def get_longest_path(self, path):
        print(len(path))
        pos = path[-1]
        if pos == self.finish:
            return path
        neighbors = self.get_available_neighbors(path)
        longest_n_path = []
        for neighbor in neighbors:
            n_path = self.get_longest_path(path + [neighbor])
            if len(n_path) > len(longest_n_path):
                longest_n_path = n_path
        return longest_n_path

    def get_longest_path_distance(self):
        path = self.get_longest_path(path=[(1, 1)])
        print(path)
        return len(path)


if __name__ == "__main__":
    # input_file_path = "day23/test_input.txt"
    input_file_path = "day23/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    # part1
    print(app.get_longest_path_distance())
