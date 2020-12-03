import networkx as nx

def find_uip(g, current_decision_node):
    s = {current_decision_node}
    while len(s) != 0:
        s_temp = set()
        for node in s:
           for n in list(g.successors(node)):
               s_temp.add(n)
        s = s_temp
        if len(s) == 1 and list(g.successors(list(s)[0])) != []:
            uid = s
    print(uid.pop())

# DG = nx.DiGraph()
# DG.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
# DG.add_edges_from([(1,5),(4,6),(4,5),(6,7),(5,7),(7,8),(7,9),(2,9),(9,10),(8,10)])
#
# find_uip(DG, 4)

# DG = nx.DiGraph()
# DG.add_nodes_from([1,2,3,4,5,6,7,8,'c'])
# DG.add_edges_from([(8,6),(7,5),(5,4),(6,4),(4,3),(4,'c'),(3,'c'),(2,'c'),(1,2)])
# find_uip(DG, 7)

# DG = nx.DiGraph()
# DG.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
# from Solver import Claus
# from Formula import Formula
# DG.add_edge(1, 2, weight=Claus(Formula("q")))
# c = DG.edges[1,2]['weight']
# print(c)