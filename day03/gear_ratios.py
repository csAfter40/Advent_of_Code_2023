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

    def get_wrapped_matrix(self, char):
        wrapped_matrix = []
        first_last_line = ["." for _ in range(len(self.matrix[0]) + 2)]
        wrapped_matrix.append(first_last_line)
        for row in self.matrix:
            wrapped_matrix.append(["."] + row + ["."])
        wrapped_matrix.append(first_last_line)
        return wrapped_matrix


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.parser_class = parser_class
        self.data = []

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        """
        Reads input and setup data.
        """
        for line in self.get_lines():
            self.data.append(line)
        parser = self.parser_class(self.data)
        self.matrix = parser.get_wrapped_matrix(".")

    def is_valid_part_number(self, start, end):
        # check top
        for i in range(start[1] - 1, end[1] + 2):
            if self.matrix[start[0] - 1][i] != ".":
                return True
        # check sides
        if self.matrix[start[0]][start[1] - 1] != ".":
            return True
        if self.matrix[end[0]][end[1] + 1] != ".":
            return True
        # check bottom
        for i in range(start[1] - 1, end[1] + 2):
            if self.matrix[start[0] + 1][i] != ".":
                return True
        return False

    def get_valid_numbers(self):
        valid_numbers = []
        for j, row in enumerate(self.matrix):
            number_start_coordinates = None
            number_end_coordinates = None
            number = ""
            for i, char in enumerate(row):
                if char.isnumeric():
                    if number_start_coordinates == None:
                        number_start_coordinates = (j, i)
                    number += char
                else:
                    if number_start_coordinates:
                        number_end_coordinates = (j, i - 1)
                        if self.is_valid_part_number(
                            number_start_coordinates, number_end_coordinates
                        ):
                            valid_numbers.append(int(number))
                        number_start_coordinates = None
                        number_end_coordinates = None
                        number = ""
        return valid_numbers

    def calculate_valid_number_sum(self):
        return sum(self.get_valid_numbers())

    def get_gear_star(self, start, end):
        # check top
        for i in range(start[1] - 1, end[1] + 2):
            if self.matrix[start[0] - 1][i] == "*":
                return (start[0] - 1, i)
        # check sides
        if self.matrix[start[0]][start[1] - 1] == "*":
            return (start[0], start[1] - 1)
        if self.matrix[end[0]][end[1] + 1] == "*":
            return (end[0], end[1] + 1)
        # check bottom
        for i in range(start[1] - 1, end[1] + 2):
            if self.matrix[start[0] + 1][i] == "*":
                return (start[0] + 1, i)
        return None

    def get_gears(self):
        gear_stars = {}
        gears = []
        for j, row in enumerate(self.matrix):
            number_start_coordinates = None
            number_end_coordinates = None
            number = ""
            for i, char in enumerate(row):
                if char.isnumeric():
                    if number_start_coordinates == None:
                        number_start_coordinates = (j, i)
                    number += char
                else:
                    if number_start_coordinates:
                        number_end_coordinates = (j, i - 1)
                        gear_star = self.get_gear_star(
                            number_start_coordinates, number_end_coordinates
                        )
                        if gear_star:
                            if gear_star in gear_stars:
                                gears.append((gear_stars[gear_star], int(number)))
                            else:
                                gear_stars[gear_star] = int(number)

                        number_start_coordinates = None
                        number_end_coordinates = None
                        number = ""
        print(gears)
        return gears

    def calculate_gear_ratio_sum(self):
        gears = self.get_gears()
        return sum([gear[0] * gear[1] for gear in gears])

    def print_matrix(self):
        for row in self.matrix:
            print(*row, sep="")


if __name__ == "__main__":
    input_file_path = "day03/input.txt"
    app = App(input_file_path, MatrixParser)
    app.setup_data()
    app.print_matrix()
    print(app.calculate_valid_number_sum())
    print(app.calculate_gear_ratio_sum())
