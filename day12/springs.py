from functools import cache
import tracemalloc


class SpringParser:
    def __init__(self, lines):
        self.lines = lines
        self.records = []

    def parse(self):
        for line in self.lines:
            springs, sizes = line.split()
            sizes = (*[int(num) for num in sizes.split(",")],)
            self.records.append((springs, sizes))
        return self.records


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.lines = []
        self.parser_class = parser_class

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        for line in self.get_lines():
            self.lines.append(line)
        parser = self.parser_class(self.lines)
        self.records = parser.parse()
        self.set_folded_records()

    def set_folded_records(self):
        self.folded_records = []
        for record in self.records:
            springs, sizes = record
            folded_springs = "?".join([springs] * 5)
            folded_sizes = sizes * 5
            self.folded_records.append((folded_springs, folded_sizes))

    def get_sizes_length(self, sizes):
        return sum(sizes) + len(sizes) - 1

    def is_proper(self, springs, size, i):
        if i > 0 and springs[i - 1] == "#":
            return False
        if "." in springs[i : i + size]:
            return False
        if i + size < len(springs) and springs[i + size] == "#":
            return False
        return True

    def has_no_remaining_spring(self, springs, size, i):
        for j, char in enumerate(springs):
            if j in range(i, i + size):
                continue
            elif char == "#":
                return False
        return True

    @cache
    def get_arrangement_quantity(self, record):
        total = 0
        springs, sizes = record
        sizes_len = self.get_sizes_length(sizes)
        start = 0
        try:
            end = min(len(springs) - sizes_len, springs.index("#") + 1)
        except ValueError:
            end = len(springs) - sizes_len
        for i in range(end + 1):
            if self.is_proper(springs, sizes[0], i):
                if len(sizes) > 1:
                    sub_record = (springs[sizes[0] + i + 1 :], (sizes[1:]))
                    total += self.get_arrangement_quantity(sub_record)
                else:
                    if self.has_no_remaining_spring(springs, sizes[0], i):
                        total += 1
        return total

    def get_total_arrangement_quantity(self):
        total = 0
        for record in self.records:
            total += self.get_arrangement_quantity(record)
        return total

    def get_total_folded_arrangement_quantity(self):
        total = 0
        for i, record in enumerate(self.folded_records):
            total += self.get_arrangement_quantity(record)
        return total


if __name__ == "__main__":
    # tracemalloc.start()
    # input_file_path = "day12/test_input.txt"
    input_file_path = "day12/input.txt"
    app = App(input_file_path, SpringParser)
    app.setup_data()
    # Part 1
    print(app.get_total_arrangement_quantity())
    # Part 2
    print(app.get_total_folded_arrangement_quantity())

    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics("lineno")
    # print("[ Top 10 ]")
    # for stat in top_stats[:10]:
    #     print(stat)
