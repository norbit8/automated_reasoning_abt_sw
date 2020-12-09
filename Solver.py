import copy
from typing import *
from Formula import Formula, is_binary, is_unary
from semantics import evaluate, is_satisfiable
import sys
import Parser
from Bcp import Bcp, PART_A_BCP, PART_B_BCP
from collections import Counter

# constants
UNSAT_STATE = 0
BCP_OK = 1
ADD_CONFLICT_CLAUS = 2


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
        return (False, False)
    else:
        return (satisfiable, [(k, v) for k, v in assignment_map.items()])


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


def count_variables(f):
    l = []
    for claus in f:
        l += claus.variables
    return len(set(l))


def get_literal_list(f):
    literal_list = []
    for claus in f:
        literal_list += claus.literals
    return literal_list


def dlis(assignmet_map, f):
    counter = Counter(get_literal_list(f))
    for key in assignmet_map.keys():
        del counter[key]
        del counter["~" + key]
    literal = max(counter, key=counter.get)
    if literal[0] == "~":
        return (literal[1:], False)
    else:
        return (literal, True)


def get_variable_list(f):
    literal_list = []
    for claus in f:
        literal_list += claus.variables
    return set(literal_list)


def assign_true_assingment(assignmet_map, f):
    literals = list(get_variable_list(f) - set(assignmet_map.keys()))
    literals.sort()
    return literals[0], True


def part_A(f):
    # pre-proccsing
    satsfible, assignmet_map = get_initial_assignment(f)
    if not satsfible:
        print("UNSAT")
        return (False, False)

    # creating watch literal map
    watch_literal_map = creates_watch_literals(f)
    # PART A
    bcp = Bcp(watch_literal_map.copy())
    state, response = bcp.bcp_step(assignmet_map,
                                   PART_A_BCP)  # (msg_type(int), content) type: 0 - unsat, 1 - assignment, 2- conflict clause
    if (state == UNSAT_STATE):
        print("UNSAT!")
        return (False, False)
    elif (state == BCP_OK):
        assignmet_map = response
        return (True, (watch_literal_map, assignmet_map, bcp))


def main(input_formula):
    # cretes Tsieni
    f = Parser.parse(input_formula)
    formula_original = copy.deepcopy(f)
    # number of variables in formula
    N = count_variables(f)
    state, response = part_A(f)
    if state == UNSAT_STATE:
        return False
    else:
        watch_literal_map, assignmet_map, bcp = response
    # PART B
    while len(assignmet_map.keys()) < N:
        chosen_literal, chosen_assignment = dlis(assignmet_map.copy(), f)
        # chosen_literal, chosen_assignment = assign_true_assingment(assignmet_map.copy(), f) #TODO remove
        state, response = bcp.bcp_step([(chosen_literal, chosen_assignment)], PART_B_BCP)
        if (state == ADD_CONFLICT_CLAUS):
            # build watch literal for claus add calus to formula and go back to line 104
            formula_original.append(response)
            f = copy.deepcopy(formula_original)
            state, response = part_A(f)
            if state == UNSAT_STATE:
                return False
            else:
                watch_literal_map, assignmet_map, bcp = response
        elif (state == BCP_OK):
            assignmet_map = response
    print("SAT!", assignmet_map)


if __name__ == '__main__':
    # building input sxample
    # main('sys.argv[1]')
    # print(is_satisfiable(f))
    # main("((p|q)<->~(p|q))")
    main("(((((p1->p2)<->(q&p1))&((p33->p12)<->(q3&p4)))|(((p14->p8)<->(q512&p64))&((p82->p79)<->(q555&p95))))<->~((((p1->p2)<->(q&p1))&((p33->p12)<->(q3&p4)))|(((p14->p8)<->(q512&p64))&((p82->p79)<->(q555&p95)))))")
