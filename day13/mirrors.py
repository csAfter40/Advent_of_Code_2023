class PatternParser:
    def __init__(self, lines):
        self.lines = lines
        self.patterns = []

    def parse(self):
        pattern = []
        for line in self.lines:
            if line:
                pattern.append([*line])
            else:
                self.patterns.append(pattern)
                pattern = []
        self.patterns.append(pattern)
        return self.patterns

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            print(*row, sep="")


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.lines = []
        self.parser_class = parser_class
        self.mirrors = []
        self.smugged_mirrors = []

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        for line in self.get_lines():
            self.lines.append(line)
        parser = self.parser_class(self.lines)
        self.patterns = parser.parse()
        self.set_mirrors()
        self.set_smugged_mirrors()

    def is_mirror(self, pattern, i):
        if i == 0 or i == len(pattern) - 1:
            return True
        distance_to_edge = min(i, len(pattern) - i - 2)
        for j in range(distance_to_edge):
            if pattern[i - 1 - j] != pattern[i + 2 + j]:
                return False
        return True

    def rotate_pattern_clockwise(self, pattern):
        return [list(reversed(col)) for col in zip(*pattern)]

    def get_smudge_score(self, pattern):
        score = self.get_horizontal_qty(pattern) * 100 or self.get_vertical_qty(pattern)
        return score

    def set_horizontal_mirror(self, pattern, is_vertical=False):
        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                if self.is_mirror(pattern, i):
                    self.mirrors.append(("v" if is_vertical else "h", i))
                    return True
        return False

    def set_vertical_mirror(self, pattern):
        rotated_pattern = self.rotate_pattern_clockwise(pattern)
        return self.set_horizontal_mirror(rotated_pattern, is_vertical=True)

    def set_mirrors(self):
        for pattern in self.patterns:
            if not self.set_horizontal_mirror(pattern):
                self.set_vertical_mirror(pattern)

    def differs_by_one_item(self, seq1, seq2):
        assert len(seq1) == len(seq2)
        smudge = False
        for i in range(len(seq1)):
            if seq1[i] != seq2[i]:
                if smudge:
                    return False
                else:
                    smudge = True
        assert smudge
        return True

    def is_smugged_mirror(self, pattern, i, has_smudge=False):
        smudge = has_smudge
        if (i == 0 or i == len(pattern) - 1) and smudge:
            if not smudge:
                raise ValueError(f"another mirror without smudge! on {pattern}")
            return True
        distance_to_edge = min(i, len(pattern) - i - 2)
        for j in range(distance_to_edge):
            if pattern[i - 1 - j] != pattern[i + 2 + j]:
                if smudge:
                    return False
                elif self.differs_by_one_item(pattern[i - 1 - j], pattern[i + 2 + j]):
                    smudge = True
                else:
                    return False
        return True

    def set_horizontal_smugged_mirror(self, pattern, mirror, is_vertical=False):
        skip_index = mirror[1] if (mirror[0] == "v") == is_vertical else None
        for i in range(len(pattern) - 1):
            if i == skip_index:
                continue
            if pattern[i] == pattern[i + 1]:
                if self.is_smugged_mirror(pattern, i):
                    self.smugged_mirrors.append(("v" if is_vertical else "h", i))
                    return True
            elif self.differs_by_one_item(pattern[i], pattern[i + 1]):
                if self.is_smugged_mirror(pattern, i, has_smudge=True):
                    self.smugged_mirrors.append(("v" if is_vertical else "h", i))
                    return True
        return False

    def set_vertical_smugged_mirror(self, pattern, mirror):
        rotated_pattern = self.rotate_pattern_clockwise(pattern)
        return self.set_horizontal_smugged_mirror(
            rotated_pattern, mirror, is_vertical=True
        )

    def set_smugged_mirrors(self):
        for i, pattern in enumerate(self.patterns):
            mirror = self.mirrors[i]
            if not self.set_horizontal_smugged_mirror(pattern, mirror):
                self.set_vertical_smugged_mirror(pattern, mirror)

    def get_summary(self, is_smugged=False):
        total = 0
        mirrors = self.smugged_mirrors if is_smugged else self.mirrors
        for mirror in mirrors:
            if mirror[0] == "h":
                total += 100 * (mirror[1] + 1)
            else:
                total += mirror[1] + 1
        return total


if __name__ == "__main__":
    # input_file_path = "day13/test_input.txt"
    input_file_path = "day13/input.txt"
    app = App(input_file_path, PatternParser)
    app.setup_data()
    print(app.get_summary())
    print(app.get_summary(is_smugged=True))
