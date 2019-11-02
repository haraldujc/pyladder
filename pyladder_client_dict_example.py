# This is a sample client calling the graph rendering engine with a dictionary of nodes.
# This convention invokes pyladder to visually display the graph.
# The dictionary key is the descriptor of a node that will be displayed along the y axis
# The dictionary value is a list of nodes, where the first is the node that corresponds to the descriptor in the key,
# and subsequent list elements are the nodes to which it connects

from pyladder import Pyladder

# Planar ladder
ladder_input = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}

# Non-planar ladder
# ladder_input = {'Part A' : [10,20,90,120], 'Part B' : [20,30, 100], 'Part C' : [30, 40, 120], 'Part D' : [40,50,80,90], 'Part E' : [50,60,120], 'Part F' : [60,70,100], 'Part G' : [70,80]}

my_ladder = Pyladder()
if my_ladder.display_graph_plot('dictionary input example', 'ladder step', ladder_input, True):
    print("Ladder is planar")
else:
    print("Ladder is not planar")

