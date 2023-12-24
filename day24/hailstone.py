import re


class Hailstone:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.m = vy / vx  # slope on xy

    def __repr__(self):
        return str(f"{(self.x, self.y, self.z)} @ {(self.vx, self.vy, self.vz)}")

    def get_intersection(self, other):
        if self.m == other.m:
            # they are parallel and never intersect
            return None
        x_intersection = (
            (self.m * self.x - other.m * other.x) + (other.y - self.y)
        ) / (self.m - other.m)
        y_intersection = self.m * (x_intersection - self.x) + self.y
        return (x_intersection, y_intersection)

    def is_future(self, pos):
        y_future = (pos[1] - self.y) / self.vy >= 0
        x_future = (pos[0] - self.x) / self.vx >= 0
        return x_future and y_future


class HailstoneParser:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        hailstones = []
        for line in self.lines:
            x, y, z, vx, vy, vz = [int(val) for val in re.split(" @ |, |,  ", line)]
            hailstones.append(Hailstone(x, y, z, vx, vy, vz))
        return hailstones


class App:
    def __init__(self, file_path, parser_class, boundaries):
        self.file_path = file_path
        self.parser_class = parser_class
        self.boundaries = boundaries

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.hailstones = parser.parse()
        # for hailstone in self.hailstones:
        #     print(hailstone)

    def within_boundaires(self, pos):
        x_min, y_min = self.boundaries[0]
        x_max, y_max = self.boundaries[1]
        return x_min <= pos[0] <= x_max and y_min <= pos[1] <= y_max

    def calculate_test_area_intersections(self):
        total = 0
        for i, hailstone1 in enumerate(self.hailstones[:-1]):
            for hailstone2 in self.hailstones[i + 1 :]:
                intersection = hailstone1.get_intersection(hailstone2)
                if not intersection:
                    continue
                if not hailstone1.is_future(intersection) or not hailstone2.is_future(
                    intersection
                ):
                    continue
                if not self.within_boundaires(intersection):
                    continue
                total += 1
        return total


if __name__ == "__main__":
    TEST_BOUNDARIES = ((7, 7), (27, 27))
    BOUNDARIES = (
        (200000000000000, 200000000000000),
        (400000000000000, 400000000000000),
    )
    # input_file_path = "day24/test_input.txt"
    input_file_path = "day24/input.txt"
    app = App(input_file_path, HailstoneParser, BOUNDARIES)
    app.setup_data()
    print(app.calculate_test_area_intersections())
