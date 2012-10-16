import random
import itertools
import networkx
import matplotlib.pyplot as plt

class Kruskal(object):
    """
    Uses Kruskal's algorithm to create a random minimum spanning tree. Assumes undirected, unweighted graph
    """

    def __init__(self, nodes, edge_list):
        """
        [nodes]  list of nodes (strings) that are in the edge_list, e.g. ['n1','n2']
        [edge_list]: list of 2-tuples whose members are nodes listed in [nodes], e.g. [ ('n1','n2'), ...]
        """
        self.nodes = nodes
        self.edge_list = edge_list
        self.treesets = [set([n]) for n in self.nodes]
        self.mst = [] #mst is an edge_list of the MST

    def _get_set(self, node):
        """
        Returns the treeset that contains [node]
        """
        return filter(lambda x: node in x, self.treesets)[0]

    def run(self):
        # apply the edges in random order
        edges = self.edge_list
        random.shuffle(edges)
        for edge in edges:
            a,b = edge
            treea = self._get_set(a)
            treeb = self._get_set(b)
            if treea != treeb:
                self.treesets.remove(treeb)
                self.treesets.remove(treea)
                treea.update(treeb)
                self.treesets.append(treea)
                self.mst.append(edge)
        return self.mst
    
    def show(self,filename=''):
        try:
            import networkx
        except ImportError:
            print "Please install networkx via 'easy_install networkx', 'pip install networkx' or some other method."
            print "You will not have access to the full functionality of this module until then"
            sys.exit(0)

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print "Please install matplotlib via 'easy_install matplotlib', 'pip install matplotlib' or some other method."
            print "You will not have access to the full functionality of this module until then"
            sys.exit(0)

        string_edges = map(lambda x: "%s %s" % (x[0], x[1]), self.mst)
        graph = networkx.parse_edgelist(string_edges)
        networkx.draw_circular(graph,prog='neato',width=1,node_size=300,font_size=14,overlap='scalexy')
        if filename:
            plt.savefig(filename)
        else:
            plt.show()
