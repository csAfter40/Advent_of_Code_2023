class App:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

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
        Given a string, finds and returns the first numeric character.
        """
        for char in line:
            try:
                return int(char)
            except ValueError:
                continue

    def get_first_digits(self):
        first_digits = []
        for line in self.data:
            first_digits.append(self.get_first_numeric(line))
        return first_digits

    def get_last_digits(self):
        last_digits = []
        for line in self.data:
            last_digits.append(self.get_first_numeric(line[::-1]))
        return last_digits

    def calculate_calibration_values_sum(self):
        first_digits = self.get_first_digits()
        last_digits = self.get_last_digits()
        return sum(first_digits) * 10 + sum(last_digits)


if __name__ == "__main__":
    app = App("Day 1/data.txt")
    app.setup_data()
    print(app.calculate_calibration_values_sum())
