class XmasParser:
    def __init__(self, lines):
        self.lines = lines
        self.functions = {
            ">": (lambda part, num: part > num),
            "<": (lambda part, num: part < num),
        }

    def setup_workflows(self, lines):
        workflows = {}
        for line in lines:
            name, flow_string = line[:-1].split("{")
            rules = []
            for item in flow_string.split(","):
                rule = {}
                logic_text = ""
                try:
                    logic_text, destination = item.split(":")
                except ValueError:
                    destination = item
                rule["destination"] = destination
                if logic_text:
                    if "<" in logic_text:
                        property, num = logic_text.split("<")
                        logic = {
                            "property": property,
                            "function": self.functions["<"],
                            "num": int(num),
                        }
                    if ">" in logic_text:
                        property, num = logic_text.split(">")
                        logic = {
                            "property": property,
                            "function": self.functions[">"],
                            "num": int(num),
                        }
                    rule["logic"] = logic
                rules.append(rule)
            workflows[name] = rules
        return workflows

    def setup_parts(self, lines):
        parts = []
        for line in lines:
            x, m, a, s = line[1:-1].split(",")
            part = {
                "x": int(x.split("=")[1]),
                "m": int(m.split("=")[1]),
                "a": int(a.split("=")[1]),
                "s": int(s.split("=")[1]),
            }
            parts.append(part)
        return parts

    def parse(self):
        seperation_idx = self.lines.index("")
        workflows = self.setup_workflows(self.lines[:seperation_idx])
        parts = self.setup_parts(self.lines[seperation_idx + 1 :])
        return workflows, parts


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.parser_class = parser_class
        self.accepted = []
        self.rejected = []

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.workflows, self.parts = parser.parse()
        self.sort_parts()

    def filter(self, part, filter):
        for rule in filter:
            if "logic" in rule:
                logic = rule["logic"]
                if not logic["function"](part[logic["property"]], logic["num"]):
                    continue
            return rule["destination"]

    def sort(self, part):
        current_filter = self.workflows["in"]
        while True:
            destination = self.filter(part, current_filter)
            if destination == "A":
                self.accepted.append(part)
                break
            elif destination == "R":
                self.rejected.append(part)
                break
            else:
                current_filter = self.workflows[destination]

    def sort_parts(self):
        for part in self.parts:
            self.sort(part)

    def get_total_rating(self):
        return sum([sum(part.values()) for part in self.accepted])


if __name__ == "__main__":
    # input_file_path = "day19/test_input.txt"
    input_file_path = "day19/input.txt"
    app = App(input_file_path, XmasParser)
    app.setup_data()
    # part1
    print(app.get_total_rating())
