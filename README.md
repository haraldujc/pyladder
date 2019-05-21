# pyladder
A python library for planarity testing and rendering of ladder type graphs.  Built and tested with Python 3.7.0 32-bit

# Background:

pyladder is an exercise in translating an ANSI 'C' program to a python class.  The program will take a list of nodes representing a connected graph in the plane.  It will then attempt to generate a visual display of the graph, and advise if the graph is planar or not.

Note that as this is a learning exercise, some of the style used will not adhere to generally accepted python patterns.  There is an upper limit on the number of connections between nodes.  This is not a limitation of the algorithm, rather due to the original 'C' program being a proof-of-concept and there was no appetite for dynamic memory management and fixed arrays were used instead.

# Practical applications:

#Programmable logic controllers:
The class can be used to display a ladder representing protective interlock logic.

## Gaming:
The class can be used to render a maze or connected points in space in real time from a list of coordinates.  This is much more portable, space saving and dynamic as opposed to a fixed graphical representation in files or memory.

## Planarity testing:
The input node list could represent a list of electronic parts and the output could then be used to create an circuit board etch where the requirement is that the connecting line segments cannot cross, for obvious reasons.

Use LINK18.DAT to test a non-planar graph.

## Calling and usage convention 1:
A python dictionary describing the ladder as follows:
The key-value pair is
key = a string label identifying the node
value = a list of nodes to which this code connects.  The first element of each list is the nodes key, and the subsequent items are the keys of the nodes to which this node connects
Example :

    my_graph = pyladder()    
    graph_input_sample = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}
    my_graph.display_graph_plot('Nodes', graph_input_sample)

Note that it is up to the client to create the dictionary.  

The above will generate the following visual:

<p align="center">
  <img alt="VS Code in action" src="https://i.postimg.cc/4d26rvPD/LINK1-DAT.png">
</p>

LINK17.DAT file will display generat the following visual:

<p align="center">
  <img alt="VS Code in action" src="https://i.postimg.cc/SxmKy9jj/LINK17-DAT.png">
</p>

## Calling and usage convention 2:

Two lists containing the ladder nodes as follows:
The first list represents a node and its connections to other nodes
i.e. [x, y, z, ...] where x is the subject node and y, z, ... are the nodes to which it connects
This list is passed to the rendering engine

The second list is metadata about the first list, and is used only by matplotlib
['node description 1', 'node description 2', 'node description 3',...] where 'node description 1 mapes to 'x' in the first list
Example:

    my_graph = gp.pyladder()
    graph_input_sample = [[10,20,30,40,50], [20,30,40,50],[30,40],[40,50],[50]]
    graph_node_labels = ['Part A','Part B','Part C','Part D', 'Finish']

    my_graph.gen_graph(graph_input_sample)
    coors = my_graph.get_render()

Here, coors is a list of coordinate pair lists representing the line segments to be plotted:

[
    [[x1,y1], [x2,y2]],
    [[x3,y3], [x4,y4]],
    ...,
    [[xN,yN], [xM,yM]],
]

### Refer to pyladder_client_dict.py, pyladder_client.py and pyladder_client_file.py for usage examples

# Non-planar samples

The following files are examples on non-planar graphs:
LINK2.DAT
LINK4.DAT
LINK10.DAT
LINK18.DAT


# Issue log:

1. The label for the top 'rung' is not displayed in the matplotlib line plot.  Status = Fixed
2. The ladder representation in file LINK32.DAT is returning a 'graph rendering failed' message.   Status = Oustanding
3. Improve the visual rendering by including a marker on the vertical line segments for each level of the ladder.  This would be helpful when using the class to render PLC ladder logic.  Status = Oustanding
4. Comment out debug lines.  Presently the command line output is very verbose.  Status = Oustanding
5. File LINK36.DAT is not rendering correctly
6. File LINK20.DAT is not rendering correctly



