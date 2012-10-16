import sys
import random
import itertools
from collections import defaultdict

try:
    import networkx
except ImportError:
    print "Please install networkx via 'easy_install networkx', 'pip install networkx' or via some other method."
    print "You will not have access to the full functionality of this module until then"
    sys.exit(0)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print "Please install matplotlib via 'easy_install matplotlib', 'pip install matplotlib' or via some other method."
    print "You will not have access to the full functionality of this module until then"
    sys.exit(0)

class GGraph(object):
    def __init__(self, n=3, edge_p=.2):
        self.n = n
        self.edge_p = edge_p
        self.neighbor_list = defaultdict(list)
        self.edge_list = []


    def _make_network(self):
        # create n nodes, connected randomly
        nodes = ['n'+str(i) for i in range(1, self.n+1)]

        # create list of all possible non-self-looping edges in the graph
        possible_edges = itertools.combinations(nodes, 2)

        # create random graph
        for edge in possible_edges:
            a,b = edge
            # randomly assign edges
            if (random.random() > self.edge_p):
                self.neighbor_list[a].append(b)
                self.neighbor_list[b].append(a)
                self.edge_list.append((a,b))

        # connect any unconnected nodes
        for node in self.neighbor_list.keys():
            if len(self.neighbor_list[node]) == 0:
                self.neighbor_list[node].append(random.choice(filter(lambda x: x!=node, nodes)))
    
    def show(self):
        string_edges = map(lambda x: "%s %s" % (x[0], x[1]), self.edge_list)
        graph = networkx.parse_edgelist(string_edges)
        networkx.draw_circular(graph,prog='neato',width=1,node_size=300,font_size=14,overlap='scalexy')
        plt.show()


    def _is_leaf(self,node):
        """
        Returns True if node [node] is a leaf
        """
        return len(self.neighbor_list[node]) <= 1

    def _check_path(self,node):
        """
        Returns True if node consists the only path between any two nodes
        """
        pass
