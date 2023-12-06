import math


class App:
    def __init__(self, data):
        self.data = data

    def get_winning_interval(self, data):
        """
        If a boat goes "d" distance in a given "t" time, button release time(x) can be
        calculated by:
        x**2 - t*x + d = 0
        This function has 2 roots which are:
        (t + (t**2 - 4*d)**0.5)/2
        and
        (t - (t**2 - 4*d)**0.5)/2
        """
        t, d = data.values()
        x_min = (t - (t**2 - 4 * d) ** 0.5) / 2
        x_max = (t + (t**2 - 4 * d) ** 0.5) / 2
        return (math.floor(x_min + 1), math.ceil(x_max - 1))

    def get_winning_number_count(self, data):
        winning_interval = self.get_winning_interval(data)
        return winning_interval[1] - winning_interval[0] + 1

    def multiply_winning_number_counts(self):
        winning_number_counts = []
        for data in self.data:
            winning_number_counts.append(self.get_winning_number_count(data))
        print(winning_number_counts)
        return math.prod(winning_number_counts)


if __name__ == "__main__":
    test_data = [
        {"time": 7, "distance": 9},
        {"time": 15, "distance": 40},
        {"time": 30, "distance": 200},
    ]
    test_data_part_2 = [
        {"time": 71530, "distance": 940200},
    ]
    data = [
        {"time": 40, "distance": 215},
        {"time": 70, "distance": 1051},
        {"time": 98, "distance": 2147},
        {"time": 79, "distance": 1005},
    ]
    data_part_2 = [
        {"time": 40709879, "distance": 215105121471005},
    ]

    app = App(data_part_2)
    print(app.multiply_winning_number_counts())
