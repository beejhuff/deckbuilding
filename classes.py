from itertools import combinations

all_cards = {}


class Card():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.uprank = 0.

    def updateRank(self, num):
        self.uprank += num

    def resetRank(self):
        self.uprank = 0

    def __gt__(self, other):
        if self.name > other.name:
            return True
        if self.name == other.name and self.position < other.position:
            return True
        return False

    def __eq__(self, other):
        if self.name == other.name and self.position == other.position:
            return True
        return False

    def __ge__(self, other):
        return self > other or self == other

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return not self > other and not self == other

    def __le__(self, other):
        return self < other or self == other

    def __hash__(self):
        return hash(tuple([self.name, self.position]))

    def __repr__(self):
        return "({}, {}) : {}".format(self.name, self.position, self.uprank)


class Ranking():
    def __init__(self):
        self.rankings = {}

    def update(self, cards):
        cards = tuple(sorted(cards))
        if cards in self.rankings:
            self.rankings[cards] += 1
        else:
            self.rankings[cards] = 1

    def getNext(self):
        for cur in self.rankings.keys():
            yield cur, self.rankings[cur]

    def addDeck(self, decklist, n):  # decklist is a list of Cards
        for i in range(1, n + 1):
            for cur in combinations(decklist, i):
                self.update(sorted(cur))

    def getCollective(self):
        return set([x for y in self.rankings.keys() for x in y])


def parseDecklist(file):
    with open(file, "r") as fp:
        lines = fp.readlines()
    decklist = []
    for line in lines:
        line = line.strip()
        if line == "\n" or line == "Sideboard" or line == "":
            break
        num = int(line[:line.index(" ")])
        name = line[line.index(" ") + 1:]
        for i in range(1, num + 1):
            insert = Card(name, i)
            if insert not in all_cards:
                all_cards[insert] = insert
            decklist.append(all_cards[insert])
    return decklist
