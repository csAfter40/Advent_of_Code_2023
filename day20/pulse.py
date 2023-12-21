import math


class Module:
    def __init__(self, id, *args, **kwargs):
        self.id = id
        self.destinations = []
        self.prefix = ""

    def __str__(self):
        return f"{self.prefix}{self.id} -> {[x.id for x in self.destinations]}"

    def __repr__(self):
        return f"{self.prefix}{self.id}"

    def add_destination(self, destination):
        self.destinations.append(destination)

    def process_pulse(self, pulse):
        raise NotImplementedError


class FlipFlop(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = False
        self.prefix = "%"

    def process_pulse(self, pulse):
        responses = []
        if pulse[1] == "high":
            return []
        else:
            output = "low" if self.state else "high"
            self.state = not self.state
        for destination in self.destinations:
            responses.append((self, output, destination))
        return responses


class Conjunction(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_modules = []
        self.memo = {}
        self.prefix = "&"

    def add_input_module(self, module):
        self.input_modules.append(module)
        self.memo[module.id] = "low"

    def memo_is_high(self):
        return "low" not in self.memo.values()

    def process_pulse(self, pulse):
        responses = []
        self.memo[pulse[0].id] = pulse[1]
        output = "low" if self.memo_is_high() else "high"
        # breakpoint()
        for destination in self.destinations:
            responses.append((self, output, destination))
        return responses


class Broadcaster(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.id = "broadcaster"
        self.destinations = []

    def process_pulse(self, pulse):
        responses = []
        for destination in self.destinations:
            responses.append((self, pulse[1], destination))
        return responses


class Button(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broadcaster = kwargs["broadcaster"]

    def __str__(self):
        return f"{self.prefix}{self.id} -> {[self.broadcaster.id]}"

    def generate_pulse(self):
        return (self, "low", self.broadcaster)


class Output(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_pulse(self, pulse):
        return []


class PulseParser:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        module_map = {}
        for line in self.lines:
            module_str, destinations_str = line.split(" -> ")
            module_map[module_str] = destinations_str.split(", ")
        return module_map


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.parser_class = parser_class
        self.modules = []
        self.watch = {}

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def get_module(self, id):
        for module in self.modules:
            if module.id == id:
                return module
        raise ValueError(f"No modules with the id {id}")

    def get_modules_by_class(self, module_class):
        return filter(lambda x: isinstance(x, module_class), self.modules)

    def create_output_modules(self):
        # all_destinations = [module.destinations for module in self.modules]
        all_outputs = set(
            [id for destination in self.data.values() for id in destination]
        )
        module_ids = set([module.id for module in self.modules])
        for id in all_outputs:
            if id not in module_ids:
                self.modules.append(Output(id=id))
        # breakpoint()

    def create_module_instances(self):
        for key in self.data.keys():
            if key[0] == "&":
                module = Conjunction(id=key[1:])
            elif key[0] == "%":
                module = FlipFlop(id=key[1:])
            elif key == "broadcaster":
                module = Broadcaster(id=key)
            # else:
            #     module = Output(id=key)
            self.modules.append(module)
        self.create_output_modules()
        # self.modules.append(Output(id="output"))

    def add_module_destinations(self):
        for key, destinations in self.data.items():
            id = "broadcaster" if key == "broadcaster" else key[1:]
            module = self.get_module(id)
            for id in destinations:
                destination_module = self.get_module(id)
                module.add_destination(destination_module)

    def add_conjunction_input_modules(self):
        conjunctions = self.get_modules_by_class(Conjunction)
        for conjunction in conjunctions:
            input_modules = filter(
                lambda x: conjunction in x.destinations, self.modules
            )
            for module in input_modules:
                conjunction.add_input_module(module)

    def create_button(self):
        broadcaster = self.get_module("broadcaster")
        self.modules.append(Button("button", broadcaster=broadcaster))

    def create_modules(self):
        self.create_module_instances()
        self.add_module_destinations()
        self.add_conjunction_input_modules()
        self.create_button()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        parser = self.parser_class(lines)
        self.data = parser.parse()
        self.create_modules()
        self.button = self.get_module(id="button")

    def push_button(self):
        low_qty = 0
        high_qty = 0
        current_pulses = [self.button.generate_pulse()]
        while current_pulses:
            next_pulses = []
            for pulse in current_pulses:
                if pulse[1] == "low":
                    low_qty += 1
                else:
                    high_qty += 1
                responses = pulse[2].process_pulse(pulse)
                next_pulses.extend(responses)
            current_pulses = next_pulses
        return (low_qty, high_qty)

    def push_button_watch(self, watch):
        watched_module = None
        current_pulses = [self.button.generate_pulse()]
        while current_pulses:
            next_pulses = []
            for pulse in current_pulses:
                if pulse[0] in watch and pulse[1] == "high":
                    watched_module = pulse[0]
                responses = pulse[2].process_pulse(pulse)
                next_pulses.extend(responses)
            current_pulses = next_pulses
        return watched_module

    def is_all_flipflops_low(self):
        flip_flops = self.get_modules_by_class(FlipFlop)
        return all([module.state == False for module in flip_flops])

    def get_loop(self):
        loop = []
        i = 0
        while True:
            low_high_qty = self.push_button()
            loop.append(low_high_qty)
            i += 1
            if i == 1000:
                break
            if self.is_all_flipflops_low():
                break
        return loop

    def get_low_high_qtys(self, loop):
        low_total = high_total = 0
        for item in loop:
            low_total += item[0]
            high_total += item[1]
        return (low_total, high_total)

    def get_total_pulse_product(self, pushes):
        loop = self.get_loop()
        full_cycles = pushes // len(loop)
        incomplete_cycle = pushes % len(loop)
        low_full, high_full = self.get_low_high_qtys(loop)
        low_incomplete, high_incomplete = self.get_low_high_qtys(
            loop[:incomplete_cycle]
        )
        low_total = low_full * full_cycles + low_incomplete
        high_total = high_full * full_cycles + high_incomplete
        return low_total * high_total

    def get_pulse_frequencies(self, modules):
        matches = {}
        pushes = 0
        while True:
            watch = self.push_button_watch(watch=modules)
            pushes += 1
            if watch:
                matches[watch.id] = pushes
                if len(matches) == 4:
                    break
        return matches

    def get_min_button_pushes(self):
        # input mudules for zh module which sends pulses to rx"
        zh = self.get_module(id="zh")
        zh_input_modules = list(filter(lambda x: zh in x.destinations, self.modules))
        frequencies = self.get_pulse_frequencies(zh_input_modules)
        return math.lcm(*frequencies.values())


if __name__ == "__main__":
    # input_file_path = "day20/test_input2.txt"
    # input_file_path = "day20/test_input.txt"
    input_file_path = "day20/input.txt"
    # part 1
    app1 = App(input_file_path, PulseParser)
    app1.setup_data()
    print(app1.get_total_pulse_product(pushes=1000))
    # part 2
    app2 = App(input_file_path, PulseParser)
    app2.setup_data()
    print(app2.get_min_button_pushes())
