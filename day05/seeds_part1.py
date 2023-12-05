class AlmanacParser:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        parsed_data = {}
        current_key = None
        for line in self.lines:
            if line.startswith("seeds"):
                parsed_data["seeds"] = [int(val) for val in line.split(":")[1].split()]
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

    def get_destination_value(self, map, source_value):
        for line in self.data[map]:
            destination, source, range_value = line
            if source_value in range(source, source + range_value):
                return destination + (source_value - source)
        return source_value

    def get_seed_soil(self, seed):
        return self.get_destination_value("seed-to-soil", seed)

    def get_soil_fertilizer(self, soil):
        return self.get_destination_value("soil-to-fertilizer", soil)

    def get_fertilizer_water(self, fertilizer):
        return self.get_destination_value("fertilizer-to-water", fertilizer)

    def get_water_light(self, water):
        return self.get_destination_value("water-to-light", water)

    def get_light_temperature(self, light):
        return self.get_destination_value("light-to-temperature", light)

    def get_temperature_humidity(self, temperature):
        return self.get_destination_value("temperature-to-humidity", temperature)

    def get_humidity_location(self, humidity):
        return self.get_destination_value("humidity-to-location", humidity)

    def get_seed_location(self, seed):
        soil = self.get_seed_soil(seed)
        fertilizer = self.get_soil_fertilizer(soil)
        water = self.get_fertilizer_water(fertilizer)
        light = self.get_water_light(water)
        temperature = self.get_light_temperature(light)
        humidity = self.get_temperature_humidity(temperature)
        location = self.get_humidity_location(humidity)
        return location

    def get_locations(self):
        locations = []
        for seed in self.data["seeds"]:
            locations.append(self.get_seed_location(seed))
        return locations

    def find_lowest_location(self):
        locations = self.get_locations()
        return min(locations)


if __name__ == "__main__":
    input_file_path = "day05/test_input.txt"
    # input_file_path = "day05/input.txt"
    app = App(input_file_path, AlmanacParser)
    app.setup_data()
    print(app.find_lowest_location())
