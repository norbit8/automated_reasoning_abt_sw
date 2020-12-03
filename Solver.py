from typing import *
from Formula import Formula, is_binary, is_unary

class Claus:

    def __init__(self, formula:Formula):
        self.formula = formula
        self.literals = self.convert_to_literals(formula)
        self.number_of_literals = len(self.literals)



    def convert_to_literals(self, f):
        literals = []

        while (is_binary(f.root)):
            if (is_unary(f.first.root)):
                literals.append(f.first.root + f.first.first.root)
            else:
                literals.append(f.first.root)
            f = f.second
        if (is_unary(f.root)):
            literals.append(f.root + f.first.root)
        else:
            literals.append(f.root)
        return literals

    def __repr__(self):
        return str(self.literals)


class Literal:

    def __init__(self, variable_name:str, decision_level:int, assignment:bool):
        self.variable_name = variable_name
        self.decision_level = decision_level
        self.assignment = assignment
