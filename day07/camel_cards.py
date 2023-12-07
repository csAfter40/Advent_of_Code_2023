class Hand:
    type_coefficient = 1000000  # TODO
    types = {
        "five_of_a_kind": 7,
        "four_of_a_kind": 6,
        "full_house": 5,
        "three_of_a_kind": 4,
        "two_pair": 3,
        "one_pair": 2,
        "high_card": 1,
    }
    card_values = {
        "A": 12,
        "K": 11,
        "Q": 10,
        "J": 9,
        "T": 8,
        "9": 7,
        "8": 6,
        "7": 5,
        "6": 4,
        "5": 3,
        "4": 2,
        "3": 1,
        "2": 0,
    }
    lineups = {
        "5": "five_of_a_kind",
        "41": "four_of_a_kind",
        "32": "full_house",
        "311": "three_of_a_kind",
        "221": "two_pair",
        "2111": "one_pair",
        "11111": "high_card",
    }

    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return self.cards + ": " + str(self.get_total_value())

    def get_type(self):
        card_qtys = {}
        for card in self.cards:
            if card in card_qtys:
                card_qtys[card] += 1
            else:
                card_qtys[card] = 1
        card_lineup = "".join(
            [str(qty) for qty in sorted(card_qtys.values(), reverse=True)]
        )
        return self.lineups[card_lineup]

    def get_type_value(self):
        type = self.get_type()
        return self.types[type] * self.type_coefficient

    def get_second_order_value(self):
        total = 0
        for i, card in enumerate(self.cards):
            total += self.card_values[card] * (13 ** (4 - i))
        return total

    def get_total_value(self):
        type_value = self.get_type_value()
        second_order_value = self.get_second_order_value()
        return type_value + second_order_value


class JokerHand(Hand):
    card_values = {
        "A": 12,
        "K": 11,
        "Q": 10,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
        "J": 0,
    }

    def get_type(self):
        card_qtys = {}
        jokers = 0
        for card in self.cards:
            if card == "J":
                jokers += 1
                continue
            if card in card_qtys:
                card_qtys[card] += 1
            else:
                card_qtys[card] = 1

        card_lineup = "".join(
            [str(qty) for qty in sorted(card_qtys.values(), reverse=True)]
        )
        # in case all cards are jokers
        if not card_lineup:
            card_lineup = "0"
        if jokers:
            card_lineup = str(int(card_lineup[0]) + jokers) + card_lineup[1:]
        return self.lineups[card_lineup]


class App:
    def __init__(self, file_path, hand_class):
        self.file_path = file_path
        self.data = []
        self.hands = []
        self.hand_class = hand_class

    def get_lines(self):
        """
        Reads and yields cleaned lines from file at self.path.
        """
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()

    def parse_data(self):
        for data in self.data:
            hand, bid = data.split()
            self.hands.append((self.hand_class(hand), int(bid)))

    def setup_data(self):
        """
        Reads input and setup data.
        """
        for line in self.get_lines():
            self.data.append(line)
        self.parse_data()

    def get_sorted_hands(self):
        return sorted(self.hands, key=lambda hand: hand[0].get_total_value())

    def calculate_total_winnings(self):
        sorted_hands = self.get_sorted_hands()
        total_winnings = 0
        for i, hand in enumerate(sorted_hands):
            total_winnings += (i + 1) * hand[1]
        return total_winnings


if __name__ == "__main__":
    input_file_path = "day07/input.txt"
    # part 1
    app = App(input_file_path, Hand)
    app.setup_data()
    print(app.calculate_total_winnings())
    # part 2
    app = App(input_file_path, JokerHand)
    app.setup_data()
    print(app.calculate_total_winnings())
