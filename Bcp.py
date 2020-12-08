import networkx as nx
from typing import *
from Parser import Literal


import matplotlib.pyplot as plt


class Bcp:

    def __init__(self, watch_literals):
        self.current_graph = nx.DiGraph()
        self.current_watch_literals_map = watch_literals
        self.status = []
        self.current_assignment = dict()
        self.current_decision_level = 0
        # self.status.append((self.current_graph, self.current_watch_literals_map, self.current_assignment)) # i-th status = i-th graph, i-th watch literal
        #
        #                                                                                      # status, i-th assignment map
    def remove_watch_literal(self,variable, claus):
        if variable in self.current_watch_literals_map.keys():
            if len(self.current_watch_literals_map[variable]) == 1:
                del self.current_watch_literals_map[variable]
            else:
                self.current_watch_literals_map[variable].remove(claus)

    def update_watch_literal_map(self, new_watch_literal, claus, variable):
        self.remove_watch_literal(variable, claus)
        # print(new_watch_literal, "was here", self.current_watch_literals_map.keys())
        if new_watch_literal not in self.current_watch_literals_map.keys():

            self.current_watch_literals_map[new_watch_literal] = []
        self.current_watch_literals_map[new_watch_literal].append(claus)


    def check_for_one_bcp_assigment(self,variable):
        new_assigments = []
        #no bcp possible
        if variable not in self.current_watch_literals_map:
            return []
        stack = self.current_watch_literals_map[variable].copy()
        for claus in stack:
            claus.update_possible_literals(self.current_assignment.copy())
            # check for wasfull claus
            # print(variable, "claus", claus, "assignment", self.current_assignment, "watch", self.current_watch_literals_map)
            if not claus.is_satsfied:

                if claus.is_bcp_potential(variable):
                    # print("potential")
                    # print("pontential")
                    # print("Before: var:", variable, "claus:", claus, self.current_assignment, self.current_watch_literals_map)
                    if claus.all_false(self.current_assignment.copy(), variable):
                        # get the new bcp assignment
                        new_assigment_variable, value = claus.get_bcp_assignment(variable)
                        new_assigments.append((new_assigment_variable, value))

                        # claus.watch_literals = []

                    vars = claus.watch_literals
                    for var in vars:
                        self.remove_watch_literal(var, claus)

                    # no more watch litrals for this claus / clause is done!
                    claus.is_satsfied = True
                    claus.watch_literals = []
                    claus.possible_watch_literals = []
                    # print("After: var:", variable, "claus:", claus, self.current_assignment,
                    #       self.current_watch_literals_map)
                else:
                    # print("no potential")
                    # print("Before: var:", variable, "claus:", claus, self.current_assignment,
                    #       self.current_watch_literals_map)
                    # print(variable, claus)
                    new_watch_literal = claus.get_new_watch_literal(variable)
                    # print("new_watch:" ,new_watch_literal)
                    if new_watch_literal != []:
                        self.update_watch_literal_map(new_watch_literal, claus, variable)
                    else:
                        self.remove_watch_literal(variable, claus)
                    # print("after", self.current_watch_literals_map)
                    # print("After: var:", variable, "claus:", claus, self.current_assignment,
                    #       self.current_watch_literals_map)
        return new_assigments

    def one_bcp_step(self, variable):

        #increment decision level
        self.current_decision_level += 1


        #add node to graph
        # node = Literal(variable, self.current_decision_level, self.current_assignment[variable])
        # self.current_graph.add_node(node)

        #check for bcp step
        new_assigments = self.check_for_one_bcp_assigment(variable)
        return new_assigments

        # self.show_graph()

    def update_current_assignment(self,new_assignment):
        for var, assign in new_assignment:
            if var in self.current_assignment.keys():
                if self.current_assignment[var] != assign:
                    return False
            self.current_assignment[var] = assign
        return True

    def intialize_graph(self,new_assignment):
        nodes = []
        for variable,assign in new_assignment:
            nodes.append(Literal(variable, self.current_decision_level, assign))
            self.current_decision_level+=1
        self.current_graph.add_nodes_from(nodes)

    def bcp_step(self, new_assignment: List[Tuple[str, bool]]):
        self.update_current_assignment(new_assignment)

        stack = [(variable, assign) for variable,assign in new_assignment]
        self.intialize_graph(new_assignment)
        while stack:
            var, assign  = stack.pop()
            add_to_stack = self.one_bcp_step(var)
            # print(var, assign, add_to_stack, self.current_assignment)
            stack += add_to_stack
            if not (self.update_current_assignment(add_to_stack)):
                return (0,False)
        # print("final", self.current_watch_literals_map, self.current_assignment)
        return (1,self.current_assignment)

    def show_graph(self):
        plt.subplot(121)
        nx.draw(self.current_graph, with_labels=True, font_weight='bold')
        plt.show()


