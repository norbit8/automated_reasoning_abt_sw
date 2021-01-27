from fol.syntax import Term


class Node:
    def __init__(self, term):
        self.term = term
        self.parent = self
        self.represent = self
        self.size = 1

    def __eq__(self, other):
        return Term.__eq__(self.term, other.term)

    def __str__(self):
        return str(self.term)

    def __repr__(self):
        return str(self.term)