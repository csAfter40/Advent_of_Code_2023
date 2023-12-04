class CardParser:
    def __init__(self, data):
        self.data = data

    def parse(self):
        parsed_data = {}
        for line in self.data:
            card, numbers = line.split(":")
            winning_numbers, player_numbers = numbers.split("|")
            parsed_data[int(card.split()[1])] = (
                winning_numbers.split(),
                player_numbers.split(),
            )
        return parsed_data


class App:
    def __init__(self, file_path, parser_class):
        self.file_path = file_path
        self.data = []
        self.parser_class = parser_class
        self.card_winning_cache = {}
        self.card_sum_cache = {}

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
        parser = self.parser_class(self.data)
        self.cards = parser.parse()

    def get_winning_numbers(self, card):
        return [number for number in card[0] if number in card[1]]

    def get_card_point(self, card):
        winning_numbers = self.get_winning_numbers(card)
        qty = len(winning_numbers)
        point = 2 ** (qty - 1) if qty else 0
        return point

    def get_points(self):
        points = []
        for card in self.cards.values():
            points.append(self.get_card_point(card))
        return points

    def calculate_total_points(self):
        points = self.get_points()
        return sum(points)

    def get_winning_number_qty(self, card):
        return len(self.get_winning_numbers(card))

    def get_card_qty_sum(self, id):
        if id not in self.cards:
            return 0
        if id in self.card_sum_cache:
            return self.card_sum_cache[id]
        sum = 1
        card_numbers = self.cards[id]
        if id not in self.card_winning_cache:
            self.card_winning_cache[id] = self.get_winning_number_qty(card_numbers)
        qty = self.card_winning_cache[id]
        for i in range(qty):
            sum += self.get_card_qty_sum(id + i + 1)
        self.card_sum_cache[id] = sum
        return sum

    def calculate_card_qty(self):
        sum = 0
        for id in self.cards.keys():
            sum += self.get_card_qty_sum(id)
        return sum


if __name__ == "__main__":
    input_file_path = "day04/input.txt"
    app = App(input_file_path, CardParser)
    app.setup_data()
    print(app.calculate_total_points())
    print(app.calculate_card_qty())
