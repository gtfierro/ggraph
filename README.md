ggraph
======

Helpful functions for the creation of arbitrarily sized/connected networks (for UCB-EE122)

### Usage
To be integrated with the UCB-EE122 project, you must use `ggraph` within the context of a *scenario*.

Place the `ggraph` folder inside the folder for your project, or in some other location where it is importable. 

Import `ggraph` using 

```
import ggraph.ggraph as ggraph
```

The `ggraph` module has a factory class `GGraph` whose constructor accepts parameters that direct the probabalistic
generation of a valid network graph.

```
g = ggraph.GGraph(n, edge_p, host_p)
```

**n**: The number of *switches* in the generated network, also the upper bound on the number of hosts in the generated network.

**edge_p**: The density of edges in the resultant network; 0.0 is no edges, 1.0 is a fully connected network

**host_p**: On a range from [0.0,1.0], this multiplied by *n* is the expected number of hosts in the network.


To get the edge list for the generated network, call

```
edge_list = g.new_instance()
```

In the scenario file, we can create the switches and hosts and connect them using something like the following:

```
for edge in edge_list:
    if edge[0] not in instances:
        instances[edge[0]] = switch_type.create(edge[0]) if edge[0].startswith('s') else host_type.create(edge[0])
    if edge[1] not in instances:
        instances[edge[1]] = switch_type.create(edge[1]) if edge[1].startswith('s') else host_type.create(edge[1])

for edge in edge_list:
    instances[edge[0]].linkTo(instances[edge[1]])
```

