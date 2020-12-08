from typing import *
from Formula import Formula, is_binary, is_unary
from semantics import evaluate
import sys
import Parser
from Bcp import Bcp


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

def get_initial_assignment(f):
    satisfiable, assignment_map = check_initial_assignment(f)
    if not satisfiable:
        return (False,False)
    else:
        return (satisfiable, assignment_map)


def creates_watch_literals(f):
    """

    :param f:
    :return:
    """
    watch_literal_map = dict()
    for claus in f:
        if claus.number_of_literals > 1:
            add_watch_literals_for_clause(claus, watch_literal_map)
    return watch_literal_map

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


def main(input_formula):
    # #cretes Tsieni
    # input_formula = "((q->p)&r)"
    # f = Parser.parse(input_formula)

    c1 = Formula.parse("(~x1|(~x4|x7))") # x4 , x1
    c2 = Formula.parse("(x4|~x6)") # x4 , x6
    c3 =  Formula.parse("(~x1|~x6)") # x1, x5
    # c4 = Formula.parse("x6")
    c5 = Formula.parse("x1")

    l = [c1,c2,c3,c5]
    f = [Parser.Claus(f) for f in l]

    satsfible, assignmet_map = get_initial_assignment(f)
    if not satsfible:
        print("UNSAT")
        return False

    watch_literal_map = creates_watch_literals(f)
    bcp = Bcp(watch_literal_map)
    bcp.bcp_step(assignmet_map)


    # print("before",watch_literal_map)
    # bcp = Bcp(watch_literal_map)
    # print(bcp.one_bcp_step(('x6',True)))
    # print("after", watch_literal_map)
    #
    # bcp.one_bcp_step(('x2',True))
    # b





if __name__ == '__main__':
    main(sys.argv[1])