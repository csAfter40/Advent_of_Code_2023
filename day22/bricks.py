from functools import cache


class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start} ~ {self.end}"

    @property
    def min_z(self):
        return min(self.start[2], self.end[2])

    @property
    def max_z(self):
        return max(self.start[2], self.end[2])

    def __lt__(self, other):
        return self.min_z < other.min_z

    def get_bricks(self):
        bricks = []
        for x in range(self.end[0] - self.start[0] + 1):
            for y in range(self.end[1] - self.start[1] + 1):
                for z in range(self.end[2] - self.start[2] + 1):
                    bricks.append(
                        (self.start[0] + x, self.start[1] + y, self.start[2] + z)
                    )
        return bricks

    def get_min_bricks(self):
        if self.start[2] == self.end[2]:
            return self.get_bricks()
        return [self.start] if self.start[2] < self.end[2] else [self.end]

    def collides(self, unit):
        return unit in self.get_bricks()

    def move_down(self, qty=1):
        self.start = (self.start[0], self.start[1], self.start[2] - qty)
        self.end = (self.end[0], self.end[1], self.end[2] - qty)

    def drop_to_level(self, level):
        diff = self.min_z - level
        if diff > 0:
            self.move_down(qty=diff)


class BrickParser:
    def __init__(self, lines):
        self.lines = lines
        self.bricks = []

    def parse(self):
        for line in self.lines:
            start_str, end_str = line.split("~")
            start = tuple(int(x) for x in start_str.split(","))
            end = tuple(int(x) for x in end_str.split(","))
            self.bricks.append(Brick(start, end))
        return self.bricks


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.parser_class = parser_class

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def print_bricks(self, bricks=None):
        if not bricks:
            bricks = self.bricks
        for brick in bricks:
            print(brick)

    def bricks_can_go_down(self, brick, lower_bricks):
        if brick.min_z == 1:
            return False
        for lower_brick in lower_bricks:
            if lower_brick.max_z < brick.min_z - 1:
                continue
            for unit in brick.get_bricks():
                if lower_brick.collides((unit[0], unit[1], unit[2] - 1)):
                    return False
        return True

    def run_physics(self):
        top_level = 1
        for i, brick in enumerate(self.bricks):
            while True:
                if brick.min_z > top_level + 1:
                    brick.drop_to_level(top_level + 1)
                    continue
                if not self.bricks_can_go_down(brick, self.bricks[:i]):
                    top_level = max(brick.max_z, top_level)
                    break
                brick.move_down()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.bricks = parser.parse()
        self.bricks.sort()
        self.run_physics()
        self.bricks.sort()

    def is_on_the_ground(self, brick):
        return brick.min_z == 1

    def get_lower_bricks(self, brick):
        return list(filter(lambda x: x.max_z == brick.min_z - 1, self.bricks))

    def get_supporters(self, brick):
        lower_bricks = self.get_lower_bricks(brick)
        supporters = set()
        if not self.is_on_the_ground(brick):
            for unit in brick.get_bricks():
                for lower_brick in lower_bricks:
                    if lower_brick.collides((unit[0], unit[1], unit[2] - 1)):
                        supporters.add(lower_brick)
        return supporters

    def get_upper_bricks(self, brick):
        return list(filter(lambda x: x.min_z == brick.max_z + 1, self.bricks))

    def get_supporting(self, brick):
        upper_bricks = self.get_upper_bricks(brick)
        supporting = set()
        for unit in brick.get_bricks():
            for upper_brick in upper_bricks:
                if upper_brick.collides((unit[0], unit[1], unit[2] + 1)):
                    supporting.add(upper_brick)
        return supporting

    def is_disintegrated(self, brick):
        supporting = self.get_supporting(brick)
        for item in supporting:
            item_supporters = self.get_supporters(item)
            if len(item_supporters) < 2:
                return False
        return True

    def get_disintegrated_bricks(self):
        disintegrated_bricks = set()
        for brick in self.bricks:
            if self.is_disintegrated(brick):
                disintegrated_bricks.add(brick)
        return disintegrated_bricks

    def calculate_disintegrated_bricks(self):
        disintegrated_bricks = self.get_disintegrated_bricks()
        return len(disintegrated_bricks)

    def get_integrated_bricks(self):
        disintegrated_bricks = self.get_disintegrated_bricks()
        integrated_bricks = list(
            filter(lambda brick: brick not in disintegrated_bricks, self.bricks)
        )
        return sorted(integrated_bricks)

    # @cache
    # def get_effected_brick_qty(self, bricks):
    #     total_effected = 0
    #     supportings = set()
    #     for brick in bricks:
    #         supportings.update(self.get_supporting(brick))
    #     falling_supportings = []
    #     for supporting in supportings:
    #         supporters = self.get_supporters(supporting)
    #         if len(supporters):
    #             if all([supporter in bricks for supporter in supporters]):
    #                 falling_supportings.append(supporting)
    #     if len(falling_supportings):
    #         total_effected += len(falling_supportings) + self.get_effected_brick_qty(
    #             tuple(falling_supportings)
    #         )
    #     return total_effected

    def get_effected_brick_qty(self, brick):
        total_effected = 0
        bricks = self.bricks.copy()
        i = bricks.index(brick)
        bricks.remove(brick)
        for j, brick in enumerate(bricks):
            if self.bricks_can_go_down(brick, bricks[:j]):
                brick.move_down()
                total_effected += 1
        # if not total_effected:
        #     breakpoint()
        return total_effected

    def calculate_falling_bricks(self):
        total = 0
        integrated_bricks = self.get_integrated_bricks()
        self.print_bricks(integrated_bricks)
        for i, brick in enumerate(integrated_bricks):
            print("integrated brick: ", i)
            effected = self.get_effected_brick_qty(brick)
            if not effected:
                breakpoint()
            total += effected
            print(total)
        return total


if __name__ == "__main__":
    # input_file_path = "day22/test_input.txt"
    input_file_path = "day22/input.txt"
    app = App(input_file_path, BrickParser)
    app.setup_data()
    # part 1
    # print(app.calculate_disintegrated_bricks())
    # part 2
    print(app.calculate_falling_bricks())
