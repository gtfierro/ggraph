import sys
import random
import itertools
from collections import defaultdict
from collections import deque

import kruskal

class GGraph(object):
    """
    Class encapsulating the necessary functionality for creating arbitrarily-sized, undirected, connected
    networks.
    """
    def __init__(self, n=3, edge_p=.2, host_p=.5):
        """
        [n]: int representing the number of nodes in the graph
        [edge_p]: the probability that a given edge exists (the lower you make this number,
                  the fewer edges you are likely to have in the resultant graph)
        [host_p]: the probability that a given node is a host (defaults to switch)
        """
        self.n = n
        self.edge_p = edge_p
        self.host_p = host_p
        self.neighbor_list = defaultdict(list)
        self.edge_list = []
        # create n nodes, connected randomly
        self.nodes = ['s'+str(i) for i in range(1, self.n+1)]


    def new_instance(self):
        """
        Using the setting specified in the initialization of this GGraph, recompute the graph
        (potentially creating a new random version) and return an instance.
        """
        return self._make_network()

    def _get_edges(self,node,edge_list):
        """
        Return a list of all edges that involve [node]
        """
        return filter(lambda x: node in x, edge_list)
    
    def _edge_set_equal(self, el1, el2):
        """
        Given two lists of edges (formatted [ ('n1','n2'), ...., ('n4','n10') ]),
        return True if the lists of edges are equivalent (accounting for reordering)
        """
        el1_set = map(lambda x: set(x), el1)
        el2_set = map(lambda x: set(x), el2)
        return list(itertools.takewhile(lambda x: x in el1_set, el2_set)) == el1_set
    
    def _get_visited(self, nodes, neighbor_list):
        """
        Given a graph described by [nodes] and [neighbor_list],
        return a list of the nodes visited via DFS
        """
        first = random.choice(nodes)
        tovisit = deque()
        visited = []
        for neighbor in neighbor_list[first]:
            tovisit.appendleft(neighbor)
        while tovisit:
            current = tovisit.pop()
            if current not in visited:
                visited.append(current)
            for neighbor in neighbor_list[current]:
              if neighbor not in visited and neighbor not in tovisit:
                    tovisit.appendleft(neighbor)
        return visited

    def _make_network(self):
        """
        You shouldn't need to call this method.

        Creates the base graph, handling all the probability and checking for connectivity
        """

        # create list of all possible non-self-looping edges in the graph
        possible_edges = itertools.combinations(self.nodes, 2)

        # create random graph
        for edge in possible_edges:
            a,b = edge
            # randomly assign edges
            if (random.random() < self.edge_p):
                self.neighbor_list[a].append(b)
                self.neighbor_list[b].append(a)
                self.edge_list.append((a,b))

        # connect any unconnected nodes
        for node in self.neighbor_list.keys():
            if len(self.neighbor_list[node]) == 0:
                new_neighbor = random.choice(filter(lambda x: x!=node, self.nodes))
                self.neighbor_list[node].append(new_neighbor)
                self.neighbor_list[new_neighbor].append(node)
                self.edge_list.append((node,new_neighbor))
        
        # at this point, all nodes are in connected components, but these
        # components might not be connected

        orphaned_connected_components = []

        # do DFS from a random node, keep track of the nodes we visit
        visited = None
        while not visited:
            visited = self._get_visited(self.nodes, self.neighbor_list)
        orphaned_nodes = set(self.nodes) - set(visited)

        hopeful_orphans = []

        # each orphaned node should be part of a connected component
        for node in orphaned_nodes:
            if node not in hopeful_orphans:
                visited_orphans = self._get_visited(list(orphaned_nodes), self.neighbor_list)
                hopeful_orphans.extend(visited_orphans)
                excluded_orphans = set(orphaned_nodes) - set(visited_orphans)
                orphaned_connected_components.append(list(excluded_orphans))
        
        # for each orphan, add it to a random node in another connected component
        for cc in orphaned_connected_components:
            unfortunate_neighbor = random.choice(visited)
            lucky_orphan = random.choice(cc)
            self.neighbor_list[unfortunate_neighbor].append(lucky_orphan)
            self.neighbor_list[lucky_orphan].append(unfortunate_neighbor)
            self.edge_list.append((unfortunate_neighbor,lucky_orphan))
        
        # add minimum of 2 hosts
        for i in range(1,3):
            rand_node = random.choice(self.nodes)
            self.neighbor_list[rand_node].append('h'+str(i))
            self.edge_list.append((rand_node,'h'+str(i)))
        host_num = 3
        for i in range(len(self.nodes)):
            if random.random() < self.host_p:
                rand_node = random.choice(self.nodes)
                self.neighbor_list[rand_node].append('h'+str(host_num))
                self.edge_list.append((rand_node,'h'+str(host_num)))
                host_num += 1
        
        return self.edge_list


    def show(self, filename=''):
        """
        Uses the networkx/matplotlib.pyplot modules to graphically show what network
        was created. Nodes should have labels. Shows the resultant graph in a temporary window.
        If [filename] is provided, instead saves result in [filename]
        """
        try:
            import networkx
        except ImportError:
            print "Please install networkx via 'easy_install networkx', 'pip install networkx' or some other method."
            print "You will not have access to the full functionality of this module until then"
            sys.exit(1)

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print "Please install matplotlib via 'easy_install matplotlib', 'pip install matplotlib' or some other method."
            print "You will not have access to the full functionality of this module until then"
            sys.exit(1)

        string_edges = map(lambda x: "%s %s" % (x[0], x[1]), self.edge_list)
        graph = networkx.parse_edgelist(string_edges)
        networkx.draw_circular(graph,prog='neato',width=1,node_size=300,font_size=14,overlap='scalexy')
        if filename:
            plt.savefig(filename)
        else:
            plt.show()


    def _is_leaf(self,node):
        """
        Returns True if node [node] is a leaf
        """
        return len(self.neighbor_list[node]) == 1

    def _check_path(self,node):
        """
        Returns True if node consists the only path between any two nodes
        """
        pass
