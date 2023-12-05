class AlmanacParser:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        parsed_data = {}
        current_key = None
        for line in self.lines:
            if line.startswith("seeds"):
                values = [int(val) for val in line.split(":")[1].split()]
                parsed_data["seeds"] = [
                    values[i : i + 2] for i in range(0, len(values), 2)
                ]
                continue
            if "map" in line:
                current_key = line.split()[0]
                parsed_data[current_key] = []
            if line and line[0].isnumeric():
                parsed_data[current_key].append([int(val) for val in line.split()])

        return parsed_data


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.lines = []
        self.parser_class = parser_class

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
            self.lines.append(line)
        parser = self.parser_class(self.lines)
        self.data = parser.parse()

    def get_in_out_ranges(self, line, source_range):
        in_ranges = []
        out_ranges = []
        destination, source, range_value = line
        line_range = [source, source + range_value - 1]
        # check if ranges completely discrete
        if source_range[1] < line_range[0] or source_range[0] > line_range[1]:
            out_ranges.append(source_range)
        # check if line_range completely includes source_range
        if source_range[0] >= line_range[0] and source_range[1] <= line_range[1]:
            in_ranges.append(source_range)
        # check left intersect condition
        if (
            source_range[0] < line_range[0] <= source_range[1]
            and line_range[1] > source_range[1]
        ):
            in_ranges.append([line_range[0], source_range[1]])
            out_ranges.append([source_range[0], line_range[0] - 1])
        # check right intersect condition
        if (
            line_range[0] < source_range[0] <= line_range[1]
            and source_range[1] > line_range[1]
        ):
            in_ranges.append([source_range[0], line_range[1]])
            out_ranges.append([line_range[1] + 1, source_range[1]])
        # check if source_range completely includes line_range
        if source_range[0] < line_range[0] and source_range[1] > line_range[1]:
            in_ranges.append(line_range)
            out_ranges.append([source_range[0], line_range[0] - 1])
            out_ranges.append([line_range[1] + 1, source_range[1]])
        return in_ranges, out_ranges

    def calculate_destination_value(self, source_value, line):
        destination, source, range_value = line
        return (source_value - source) + destination

    def get_destination_ranges(self, in_ranges, line):
        destination_ranges = []
        for in_range in in_ranges:
            first = self.calculate_destination_value(in_range[0], line)
            second = self.calculate_destination_value(in_range[1], line)
            destination_ranges.append([first, second])
        return destination_ranges

    def get_destination_value(self, map, source_ranges):
        destination_ranges = []
        for source_range in source_ranges:
            out_ranges_container = [source_range]
            for line in self.data[map]:
                mid_out_range_container = []
                for out_range in out_ranges_container:
                    in_ranges, out_ranges = self.get_in_out_ranges(line, out_range)
                    mid_out_range_container += out_ranges
                    destination_ranges += self.get_destination_ranges(in_ranges, line)
                out_ranges_container = mid_out_range_container
            destination_ranges += out_ranges_container
        return destination_ranges

    def get_seed_soil_ranges(self, seed_ranges):
        return self.get_destination_value("seed-to-soil", seed_ranges)

    def get_soil_fertilizer_ranges(self, soil_ranges):
        return self.get_destination_value("soil-to-fertilizer", soil_ranges)

    def get_fertilizer_water_ranges(self, fertilizer_ranges):
        return self.get_destination_value("fertilizer-to-water", fertilizer_ranges)

    def get_water_light_ranges(self, water_ranges):
        return self.get_destination_value("water-to-light", water_ranges)

    def get_light_temperature_ranges(self, light_ranges):
        return self.get_destination_value("light-to-temperature", light_ranges)

    def get_temperature_humidity_ranges(self, temperature_ranges):
        return self.get_destination_value("temperature-to-humidity", temperature_ranges)

    def get_humidity_location_ranges(self, humidity_ranges):
        return self.get_destination_value("humidity-to-location", humidity_ranges)

    def get_seed_location_ranges(self, seed_ranges):
        soil_ranges = self.get_seed_soil_ranges(seed_ranges)
        fertilizer_ranges = self.get_soil_fertilizer_ranges(soil_ranges)
        water_ranges = self.get_fertilizer_water_ranges(fertilizer_ranges)
        light_ranges = self.get_water_light_ranges(water_ranges)
        temperature_ranges = self.get_light_temperature_ranges(light_ranges)
        humidity_ranges = self.get_temperature_humidity_ranges(temperature_ranges)
        location_ranges = self.get_humidity_location_ranges(humidity_ranges)
        return location_ranges

    def get_location_ranges(self):
        location_ranges = []
        for seed_value in self.data["seeds"]:
            seed_ranges = [[seed_value[0], seed_value[0] + seed_value[1] - 1]]
            location_ranges += self.get_seed_location_ranges(seed_ranges)
        return location_ranges

    def find_lowest_location(self):
        location_ranges = self.get_location_ranges()
        location_ranges = [item for item in location_ranges if item != [0, -1]]
        return min([min(location_range) for location_range in location_ranges])


if __name__ == "__main__":
    # input_file_path = "day05/test_input.txt"
    input_file_path = "day05/input.txt"
    app = App(input_file_path, AlmanacParser)
    app.setup_data()
    print(app.find_lowest_location())
