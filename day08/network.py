import re
import itertools
import math


class NetworkParser:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        parsed_data = {"instructions": "", "map": {}}
        parsed_data["instructions"] = self.lines[0]
        for line in self.lines[2:]:
            root, child1, child2 = re.split(" = \(|, ", line[:-1])
            parsed_data["map"][root] = (child1, child2)

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
        parsed_data = parser.parse()
        self.instructions = parsed_data["instructions"]
        self.map = parsed_data["map"]

    def calculate_steps(self, start, end):
        directions = itertools.cycle(self.instructions)
        total_steps = 0
        current_node = start
        for direction in directions:
            if current_node == end:
                break
            next_node = (
                self.map[current_node][0]
                if direction == "L"
                else self.map[current_node][1]
            )
            total_steps += 1
            current_node = next_node
        return total_steps

    def get_starting_nodes(self):
        return [node for node in self.map.keys() if node.endswith("A")]

    def is_valid_end_nodes(self, nodes):
        for node in nodes:
            if not node.endswith("Z"):
                return False
        return True

    def calculate_simultaneous_steps_brute_force(self):
        """Brute force is definiitely not working for large data"""
        current_nodes = self.get_starting_nodes()
        directions = itertools.cycle(self.instructions)
        total_steps = 0
        for direction in directions:
            if self.is_valid_end_nodes(current_nodes):
                break
            if direction == "L":
                next_nodes = [self.map[node][0] for node in current_nodes]
            else:
                next_nodes = [self.map[node][1] for node in current_nodes]
            total_steps += 1
            current_nodes = next_nodes
        return total_steps

    def get_node_cycle(self, node):
        directions = itertools.cycle(self.instructions)
        total_steps = 0
        current_node = node
        for direction in directions:
            if current_node.endswith("Z"):
                break
            next_node = (
                self.map[current_node][0]
                if direction == "L"
                else self.map[current_node][1]
            )
            total_steps += 1
            current_node = next_node
        return total_steps

    def calculate_simultaneous_steps(self):
        starting_nodes = self.get_starting_nodes()
        cycles = []
        for node in starting_nodes:
            cycles.append(self.get_node_cycle(node))
        return math.lcm(*cycles)


if __name__ == "__main__":
    input_file_path = "day08/input.txt"
    app = App(input_file_path, NetworkParser)
    app.setup_data()
    # part 1
    # print(app.calculate_steps(start="AAA", end="ZZZ"))
    # part 2
    print(app.calculate_simultaneous_steps())
