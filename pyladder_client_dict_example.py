# This is a sample client calling the graph rendering engine with a dictionary of nodes.
# This convention invokes graphpy to visually display the graph.
# The dictionary key is the descriptor of a node that will be displayed along the y axis
# The dictionary value is a list of nodes, where the first is the node that corresponds to the descriptor in the key,
# and subsequent list elements are the nodes to which it connects

from pyladder import Pyladder

graph_input_sample = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}

my_graph = Pyladder()
my_graph.display_graph_plot('Nodes', 'dictionary input',graph_input_sample)
