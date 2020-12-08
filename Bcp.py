import networkx as nx
from typing import *
from Solver import Literal


import matplotlib.pyplot as plt


class Bcp:

    def __init__(self, watch_literals):
        self.current_graph = nx.DiGraph()
        self.current_watch_literals_map = watch_literals
        self.status = []
        self.current_assignment = dict()
        self.current_decision_level = 0
        self.status.append((self.current_graph, self.current_watch_literals_map, self.current_assignment)) # i-th status = i-th graph, i-th watch literal

                                                                                             # status, i-th assignment map
    def remove_watch_literal(self,variable, claus):
        if len(self.current_watch_literals_map[variable]) == 1:
            del self.current_watch_literals_map[variable]
        else:
            self.current_watch_literals_map[variable].remove(claus)

    def update_watch_literal_map(self, new_watch_literal, claus, variable):
        self.remove_watch_literal(variable, claus)
        if new_watch_literal not in self.current_watch_literals_map.keys():
            self.current_watch_literals_map[new_watch_literal] = []
        self.current_watch_literals_map[new_watch_literal].append(claus)


    def check_for_one_bcp_assigment(self,variable):
        new_assigments = []
        #no bcp possible
        if variable not in self.current_watch_literals_map:
            return True
        stack = list(self.current_watch_literals_map[variable])
        for claus in stack:
            # check for wasfull claus
            if not claus.is_satsfied:
                if claus.is_bcp_potential(variable):
                    # if bcp
                    if claus.all_false(self.current_assignment, variable):
                        # get the new bcp assignment
                        new_assigment_variable, value = claus.get_bcp_assignment(variable)
                        new_assigments.append((new_assigment_variable, value))
                        # no more watch litrals for this claus
                        claus.watch_literals = []
                    self.remove_watch_literal(variable, claus)
                    claus.is_satsfied = True
                else:
                    # print(variable, claus)
                    new_watch_literal = claus.get_new_watch_literal(variable)
                    self.update_watch_literal_map(new_watch_literal, claus, variable)
                    # print("after", self.current_watch_literals_map)
        return new_assigments

    def one_bcp_step(self, new_assignment: Tuple[str, bool]):
        variable, assign = new_assignment
        #increment decision level
        self.current_decision_level += 1
        #add the new assigment
        self.current_assignment[variable] = assign
        #add node to graph
        node = Literal(variable, self.current_decision_level, assign)
        self.current_graph.add_node(node)
        #check for bcp step
        new_assigments = self.check_for_one_bcp_assigment(variable)
        print("final", new_assigments)
        # self.show_graph()



    def show_graph(self):
        plt.subplot(121)
        nx.draw(self.current_graph, with_labels=True, font_weight='bold')
        plt.show()


