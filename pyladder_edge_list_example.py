# This is a sample client calling the graph rendering engine with a list of edges.
# This convention invokes pyladder to visually display the graph.

from pyladder import Pyladder

# Planar ladder
# graph_input_sample = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}
# graph_input_sample transformed into an edge list equivalent is:
ladder_edge_list = [[10,20], [10,30], [10,40], [10,50], [20,30], [20,40], [20,50], [30,40], [40,50]]

# taken from https://github.com/hagberg/planarity/
# non-planar
# ladder_edge_list = [[10, 20], [10, 30], [10, 40], [10, 50],[20, 30],[20, 40],[20, 50],[30, 40], [30, 50],[40, 50]]
# removing the first edge makes the ladder planar
# ladder_edge_list = [[10, 30], [10, 40], [10, 50],[20, 30],[20, 40],[20, 50],[30, 40], [30, 50],[40, 50]]


# Non-planar ladder
# graph_input_sample = {'Part A' : [10,20,90,120], 'Part B' : [20,30, 100], 'Part C' : [30, 40, 120], 'Part D' : [40,50,80,90], 'Part E' : [50,60,120], 'Part F' : [60,70,100], 'Part G' : [70,80]}
# graph_input_sample transformed into an edge list equivalent is:
# ladder_edge_list = [[10,20], [10,20], [10,90], [10,120], [20,30], [20,30], [20,100], [30,40], [30,120], [40,50], [40,80], [40,90], [50,60], [50,120], [60,70], [60,100], [70,80]]

my_ladder = Pyladder()

if my_ladder.display_graph_plot_edges('Nodes', 'dictionary input', ladder_edge_list):
    print("Ladder is planar")
else:
    print("Ladder is not planar")
