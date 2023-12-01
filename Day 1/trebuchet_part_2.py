class App:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.digit_map = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }

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
            self.data.append(line)

    def get_first_numeric(self, line):
        """
        Given a string, finds and returns the first numeric string.
        """
        num = None
        first_index = len(line)
        for key, value in self.digit_map.items():
            index = line.find(key)
            if -1 < index < first_index:
                num = value
                first_index = index
        return num

    def get_last_numeric(self, line):
        """
        Given a string, finds and returns the last numeric string.
        """
        num = None
        last_index = -1
        for key, value in self.digit_map.items():
            index = line.rfind(key)
            if last_index < index:
                num = value
                last_index = index

        print(line, num)

        return num

    def get_first_digits(self):
        first_digits = []
        for line in self.data:
            first_digits.append(self.get_first_numeric(line))
        return first_digits

    def get_last_digits(self):
        last_digits = []
        for line in self.data:
            last_digits.append(self.get_last_numeric(line))
        return last_digits

    def calculate_calibration_values_sum(self):
        first_digits = self.get_first_digits()
        last_digits = self.get_last_digits()
        return sum(first_digits) * 10 + sum(last_digits)


if __name__ == "__main__":
    app = App("Day 1/data.txt")
    app.setup_data()
    print(app.calculate_calibration_values_sum())
