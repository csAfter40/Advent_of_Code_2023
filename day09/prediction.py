class App:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.direction = "forward"

    def get_lines(self):
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def setup_data(self):
        for line in self.get_lines():
            self.data.append([int(item) for item in line.split()])

    def get_differences(self, sequence):
        differences = []
        for i in range(len(sequence) - 1):
            differences.append(sequence[i + 1] - sequence[i])
        return differences

    def get_forward_prediction(self, sequence):
        if not any(sequence):
            return 0
        next_sequence = self.get_differences(sequence)
        return sequence[-1] + self.get_forward_prediction(next_sequence)

    def get_backward_prediction(self, sequence):
        if not any(sequence):
            return 0
        next_sequence = self.get_differences(sequence)
        return sequence[0] - self.get_backward_prediction(next_sequence)

    def get_predictions(self):
        predictions = []
        for sequence in self.data:
            if self.direction == "forward":
                predictions.append(self.get_forward_prediction(sequence))
            elif self.direction == "backward":
                predictions.append(self.get_backward_prediction(sequence))
        return predictions

    def get_sum_of_predictions(self):
        return sum(self.get_predictions())


if __name__ == "__main__":
    input_file_path = "day09/input.txt"
    app = App(input_file_path)
    app.setup_data()
    # part 1
    print(app.get_sum_of_predictions())
    # part 2
    app.direction = "backward"
    print(app.get_sum_of_predictions())
