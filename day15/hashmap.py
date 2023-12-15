from collections import OrderedDict


class App:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.boxes = {}

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        lines = []
        for line in self.get_lines():
            lines.append(line)
        self.data = lines[0].split(",")
        self.set_boxes()

    def get_hash_value(self, step):
        """
        * Determine the ASCII code for the current character of the string.
        * Increase the current value by the ASCII code you just determined.
        * Set the current value to itself multiplied by 17.
        * Set the current value to the remainder of dividing itself by 256.
        """
        value = 0
        for char in step:
            value += ord(char)
            value *= 17
            value = value % 256
        return value

    def perform_update_or_create(self, step):
        lens, value = step.split("=")
        value = int(value)
        hash = self.get_hash_value(lens)
        if hash in self.boxes:
            self.boxes[hash][lens] = value
        else:
            self.boxes[hash] = OrderedDict([(lens, value)])

    def perform_remove(self, step):
        lens = step.split("-")[0]
        hash = self.get_hash_value(lens)
        try:
            self.boxes[hash].pop(lens)
        except KeyError:
            pass

    def set_boxes(self):
        for step in self.data:
            if "-" in step:
                self.perform_remove(step)
            else:
                self.perform_update_or_create(step)

    def get_hash_sum(self):
        total = 0
        for step in self.data:
            total += self.get_hash_value(step)
        return total

    def get_focusing_power(self, box, slots):
        """
        One plus the box number of the lens in question.
        The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
        The focal length of the lens.

        rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
        cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
        ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
        ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
        pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72
        """
        power = 0
        for slot_idx, focal_length in enumerate(slots.values()):
            power += (box + 1) * (slot_idx + 1) * focal_length
        return power

    def get_total_focusing_power(self):
        total = 0
        for box, slots in self.boxes.items():
            if not slots:
                continue
            total += self.get_focusing_power(box, slots)
        return total


if __name__ == "__main__":
    # input_file_path = "day15/test_input.txt"
    input_file_path = "day15/input.txt"
    app = App(input_file_path)
    app.setup_data()
    # part 1
    print(app.get_hash_sum())
    # part 2
    print(app.get_total_focusing_power())
