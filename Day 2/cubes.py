class CubeDataParser:
    def __init__(self, data):
        self.data = data

    def get_game_id(self, game):
        return int(game.split()[1])

    def get_set(self, record):
        set = {}
        color_counts = record.split(",")
        for color_count in color_counts:
            qty, color = color_count.strip().split()
            set[color] = int(qty)
        return set

    def get_sets(self, records):
        sets = []
        records = records.split(";")
        for record in records:
            set = self.get_set(record)
            sets.append(set)
        return sets

    def parse(self):
        parsed_data = {}
        for line in self.data:
            game, records = line.split(":")
            game_id = self.get_game_id(game)
            sets = self.get_sets(records)
            parsed_data[game_id] = sets
        return parsed_data


class App:
    def __init__(self, file_path, parser_class, limits):
        self.file_path = file_path
        self.data = []
        self.parser_class = parser_class
        self.parsed_data = None
        self.limits = limits

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup(self):
        """
        Reads input and setup data.
        """
        for line in self.get_lines():
            self.data.append(line)
        parser = self.parser_class(self.data)
        self.parsed_data = parser.parse()

    def is_valid_set(self, set):
        return (
            set.get("red", 0) <= self.limits["red"]
            and set.get("blue", 0) <= self.limits["blue"]
            and set.get("green", 0) <= self.limits["green"]
        )

    def is_valid_sets(self, sets):
        for set in sets:
            if not self.is_valid_set(set):
                return False
        return True

    def get_valid_id_list(self):
        valid_id_list = []
        for id, sets in self.parsed_data.items():
            if self.is_valid_sets(sets):
                valid_id_list.append(id)
        return valid_id_list

    def calculate_id_sum(self):
        valid_id_list = self.get_valid_id_list()
        return sum(valid_id_list)

    def get_fewest_numbers(self, sets):
        fewest_numbers = {"red": 0, "blue": 0, "green": 0}
        for set in sets:
            for color, value in set.items():
                if fewest_numbers[color] < value:
                    fewest_numbers[color] = value
        return fewest_numbers

    def get_power(self, sets):
        fewest_numbers = self.get_fewest_numbers(sets)
        red_qty = fewest_numbers.get("red", 0)
        blue_qty = fewest_numbers.get("blue", 0)
        green_qty = fewest_numbers.get("green", 0)
        return red_qty * blue_qty * green_qty

    def get_power_list(self):
        power_list = []
        for sets in self.parsed_data.values():
            power = self.get_power(sets)
            power_list.append(power)
        return power_list

    def calculate_power_sum(self):
        power_list = self.get_power_list()
        return sum(power_list)


if __name__ == "__main__":
    cube_limits = {"red": 12, "green": 13, "blue": 14}
    input_file_path = "Day 2/input.txt"
    app = App(input_file_path, CubeDataParser, cube_limits)
    app.setup()
    print("part 1: ", app.calculate_id_sum())
    print("part 2: ", app.calculate_power_sum())
