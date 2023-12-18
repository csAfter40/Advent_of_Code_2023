def print_matrix(matrix):
    for row in matrix:
        print(*row, sep="")


class DigPlanHexParser:
    def __init__(self, lines):
        self.lines = lines
        self.direction_map = {
            "0": (0, 1),
            "1": (1, 0),
            "2": (0, -1),
            "3": (-1, 0),
        }

    def parse(self):
        data = []
        for line in self.lines:
            hex_code = line.split()[2][1:-1]
            direction = self.direction_map[hex_code[-1]]
            distance = int(hex_code[1:-1], 16)
            data.append((direction, distance))
        return data


class DigPlanParser:
    def __init__(self, lines):
        self.lines = lines
        self.direction_map = {
            "R": (0, 1),
            "L": (0, -1),
            "U": (-1, 0),
            "D": (1, 0),
        }

    def parse(self):
        data = []
        for line in self.lines:
            direction_char, distance, color = line.split()
            data.append((self.direction_map[direction_char], int(distance)))
        return data


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.data = []
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
        self.data = parser.parse()
        self.polygon = self.setup_polygon()

    def setup_polygon(self):
        polygon = []
        current_pos = (0, 0)
        for item in self.data:
            polygon.append(current_pos)
            direction, distance = item
            current_pos = (
                current_pos[0] + direction[0] * distance,
                current_pos[1] + direction[1] * distance,
            )
        polygon.append(current_pos)
        return polygon

    def get_polygon_area(self):
        """
        https://en.wikipedia.org/wiki/Shoelace_formula
        Area = 0.5 × |x1y2 - y1x2 + x2y3 - y2x3 + ... + xny1 - ynx1|
        """
        sum = 0
        perimeter = 0
        for i in range(len(self.polygon) - 1):
            vertice_1 = self.polygon[i]
            vertice_2 = self.polygon[i + 1]
            sum += vertice_1[1] * vertice_2[0] - vertice_1[0] * vertice_2[1]
            perimeter += self.data[i][1]
        area = abs(sum) / 2
        return int(area + perimeter / 2 + 1)


if __name__ == "__main__":
    # input_file_path = "day18/test_input.txt"
    input_file_path = "day18/input.txt"
    # Part 1
    app1 = App(input_file_path, DigPlanParser)
    app1.setup_data()
    print(app1.get_polygon_area())
    # Part 2
    app1 = App(input_file_path, DigPlanHexParser)
    app1.setup_data()
    print(app1.get_polygon_area())
