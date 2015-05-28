class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        if self.number == '10':
            return 'T' + self.color[0].lower()
        return self.number + self.color[0].lower()
