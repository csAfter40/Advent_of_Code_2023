class XmasRangeParser:
    def __init__(self, lines):
        self.lines = lines

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
                            "operator": "<",
                            "num": int(num),
                        }
                    if ">" in logic_text:
                        property, num = logic_text.split(">")
                        logic = {
                            "property": property,
                            "operator": ">",
                            "num": int(num),
                        }
                    rule["logic"] = logic
                rules.append(rule)
            workflows[name] = rules
        return workflows

    def parse(self):
        seperation_idx = self.lines.index("")
        workflows = self.setup_workflows(self.lines[:seperation_idx])
        return workflows


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.parser_class = parser_class
        self.accepted = []

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.workflows = parser.parse()

    def get_part_combination(self, part):
        if not part:
            return 0
        product = 1
        for interval in part.values():
            product *= interval[1] - interval[0] + 1
        return product

    def get_new_parts_lt(self, part, property, num):
        if part[property][0] >= num:
            return None, part
        elif part[property][1] < num:
            return part, None
        else:
            part_passes = part.copy()
            part_passes[property] = (part[property][0], num - 1)
            part_fails = part.copy()
            part_fails[property] = (num, part[property][1])
            return part_passes, part_fails

    def get_new_parts_gt(self, part, property, num):
        if part[property][0] > num:
            return part, None
        elif part[property][1] <= num:
            return None, part
        else:
            part_passes = part.copy()
            part_passes[property] = (num + 1, part[property][1])
            part_fails = part.copy()
            part_fails[property] = (part[property][0], num)
            return part_passes, part_fails

    def get_all_combinations_qty(self, part, workflow_id):
        if not part:
            return 0
        rules = self.workflows[workflow_id]
        sum = 0
        current_part = part
        for rule in rules:
            destination = rule["destination"]
            if "logic" in rule:
                logic = rule["logic"]
                if logic["operator"] == "<":
                    part_passes, part_fails = self.get_new_parts_lt(
                        current_part, logic["property"], logic["num"]
                    )
                else:
                    part_passes, part_fails = self.get_new_parts_gt(
                        current_part, logic["property"], logic["num"]
                    )
                if destination == "A":
                    sum += self.get_part_combination(part_passes)
                elif destination != "R":
                    sum += self.get_all_combinations_qty(part_passes, destination)
                if not part_fails:
                    break
                current_part = part_fails
            else:
                if destination == "A":
                    sum += self.get_part_combination(current_part)
                elif destination == "R":
                    continue
                else:
                    sum += self.get_all_combinations_qty(current_part, destination)

        return sum

    def get_all_combinations_qty_init(self):
        part = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
        workflow_id = "in"
        return self.get_all_combinations_qty(part, workflow_id)


if __name__ == "__main__":
    # input_file_path = "day19/test_input.txt"
    input_file_path = "day19/input.txt"
    app = App(input_file_path, XmasRangeParser)
    app.setup_data()
    # part2
    print(app.get_all_combinations_qty_init())
