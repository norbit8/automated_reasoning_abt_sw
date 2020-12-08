from __future__ import annotations
from typing import *
from Formula import Formula, is_binary, is_unary
from semantics import evaluate


class Claus:

    def __init__(self, formula:Formula):
        self.formula = formula
        self.literals = self.convert_to_literals(formula)
        self.number_of_literals = len(self.literals)
        self.variables = list(self.formula.variables())
        self.possible_watch_literals = self.variables
        self.watch_literals = []
        self.is_satsfied = False

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

    def get_last_one(self):
        if self.number_of_literals == 1:
            return self.literals[0][0] != "~"

    def conatin_variabe(self, variable:str):
        return variable in self.variables

    def get_one_watch_literal(self):
        return self.possible_watch_literals.pop(0)

    def get_two_watch_literals(self):
        return self.possible_watch_literals[:2]

    def is_bcp_potential(self, variable):
        return len(self.possible_watch_literals) == 0 and len(list(set(self.watch_literals) - {variable})) == 1

    def get_new_watch_literal(self, variable):
        self.watch_literals.remove(variable)
        new_watch_literal = [self.get_one_watch_literal(),]
        self.watch_literals += new_watch_literal
        return new_watch_literal[0]

    def get_literal(self, variable):
        for literal in self.literals:
            if variable in literal:
                return literal
        #error
        print("problem1")
        exit(1)

    def all_false(self,model, variable):
        last_unassinged_literal = (set(self.watch_literals) - {variable}).pop()
        literal = self.get_literal(last_unassinged_literal)
        if literal[0] == '~':
            model[last_unassinged_literal] = True
        else:
            model[last_unassinged_literal] = False
        return not evaluate(self.formula, model)

    def get_bcp_assignment(self, variable):
        last_unassinged_literal = (set(self.watch_literals) - {variable}).pop()
        literal = self.get_literal(last_unassinged_literal)
        if literal[0] == '~':
            value = False
        else:
           value = True
        return last_unassinged_literal, value

    def __repr__(self):
        return str(self.literals)


class Literal:

    def __init__(self, variable_name:str, decision_level:int, assignment:bool):
        self.variable_name = variable_name
        self.decision_level = decision_level
        self.assignment = assignment

    def __eq__(self, other: Literal):
        return self.variable_name == other.variable_name

    def __hash__(self):
        return self.variable_name.__hash__()

    def __repr__(self):
        return self.variable_name

def get_watch_literals_for_clause(claus):
    claus.watch_literals = claus.get_two_watch_literals()
    claus.possible_watch_literals = list(set(claus.possible_watch_literals) - set(claus.watch_literals))
    return claus.watch_literals


def add_watch_literals_for_clause(claus, watch_literal_map):
    literals_list = get_watch_literals_for_clause(claus)
    for lit in literals_list:
        if lit not in watch_literal_map.keys():
            watch_literal_map[lit] = []
        watch_literal_map[lit].append(claus)

def creates_watch_literals(f):
    """

    :param f:
    :return:
    """
    satisfiable, assignment_map = check_initial_assignment(f)
    if not satisfiable:
        return False, None, None
    watch_literal_map = dict()
    for claus in f:
        if claus.number_of_literals > 1:
            add_watch_literals_for_clause(claus, watch_literal_map)
    return satisfiable, watch_literal_map, assignment_map

def check_initial_assignment(f):
    """
    function gives assignment to all clause with only one variabel and checks whether is comes to contradiction
    :param f:
    :return:
    """
    satisfiable = True
    assignment_map = dict()
    for claus in f:
        if claus.number_of_literals == 1:
            var = claus.variables[0]
            assign = claus.get_last_one()
            if var in assignment_map.keys():
                if assign != assignment_map[var]:
                    satisfiable = False
            else:
                assignment_map[var] = assign
    return satisfiable, assignment_map

