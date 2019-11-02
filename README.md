# pyladder

Harald Ujc - Screenpop Software Inc.

A python library for planarity testing and rendering of ladder type graphs.  Built with Visual Studio Code and Python 3.7.0 32-bit, 3.7.4 64-bit Conda on Windows 10 and Python 3.7.3 64-bit, 3.7.3 64-bit Conda on Mac OS X.

The algorithm is sourced from 'Efficient Planarity Testing' by John Hopcroft and Robert Tarjan

## Background

pyladder is an exercise in translating an ANSI 'C' program to a python class.  The program will take a list of nodes representing a connected graph in the plane.  It will then attempt to generate a visual display of the graph, and advise if the graph is planar or not.

Note that as this is a learning exercise, some of the style used will not adhere to generally accepted python patterns.  

There is an upper limit on the number of connections and nodes.  This is not a limitation of the algorithm, rather due to the original 'C' program being a proof-of-concept and there was no appetite for dynamic memory management and fixed arrays were used instead.

## Practical applications

### Programmable logic controllers (PLC)

The pyladder package can be used to display a ladder representing protective interlock logic.

### Gaming

The pyladder package can be used to render a maze or connected points in space in real time from a list of coordinates.  This is much more portable, space saving and dynamic as opposed to a fixed graphical representation in files or memory.

### Planarity testing

The input node list could represent a list of electronic parts and the output could then be used to create an circuit board etch where the requirement is that the connecting edges cannot cross, for obvious reasons.

Note: The pyladder package is available at the Python Package Index.
All examples below require installation of the pyladder package via:

    pip install pyladder

## Calling and usage convention 1

A python dictionary describing the ladder as follows:
The key-value pair is
key = a string label identifying the node
value = a list of nodes to which this node connects.  The first element of each list is the node key, and the subsequent items are the keys of the nodes to which this node connects
Example :

    import pyladder.pyladder as pylad
    my_ladder = pylad.Pyladder()
    ladder_input = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}
    if not my_ladder.display_graph_plot('dictionary input example', 'ladder step', ladder_input, True):
      print('Ladder is not planar')

The above code will return true or false according to the ladder planarity and will display as per below (see pyladder_client_dict_example.py for a full implementation example):

<p align="center">
  <img alt="VS Code in action" src="https://i.postimg.cc/CMQGbmTk/pyladder-dictionary-input-example.png">
</p>

LINK17.DAT file, when transformed into the dictionary format, will display as per below (the *.DAT files are discussed below, see pyladder_file_example.py):

<p align="center">
  <img alt="VS Code in action" src="https://i.postimg.cc/fyrfLvZ7/pyladder-link17-example.png">
</p>

LINK18.DAT is an example of a non-planar ladder.  A call to display_graph_plot will return False, and no visual plot will be displayed.

## Calling and usage convention 2

Two lists containing the ladder nodes as follows:
The first list represents a node and its connections to other nodes
i.e. [x, y, z, ...] where x is the subject node and y, z, ... are the nodes to which it connects

The second list is metadata about the first list, and is used only by matplotlib  ['node description 1', 'node description 2', 'node description 3',...] where 'node description 1 mapes to 'x' in the first list

Refer to pyladder_client_example.py for full implementation details

Example:

    import pyladder.pyladder as pylad

    my_ladder = pylad.Pyladder()
    ladder_input = [[10,20,30,40,50], [20,30,40,50],[30,40],[40,50],[50]]
    graph_node_labels = ['Part A','Part B','Part C','Part D', 'Finish']

    if my_ladder.gen_graph(ladder_input):
      coors = my_ladder.get_render()
    else:
      print('Ladder is not planar')

    print(coors)

The call to gen_graph will return true or false according to the ladder planarity.

Here, coors is a list of coordinate pair lists representing the line segments (edges) to be plotted.  This list in conjunction with graph_node_labels can be used with matplotlib to display the graph:

[
    [[x1,y1], [x2,y2]],
    [[x3,y3], [x4,y4]],
    ...,
    [[xN,yN], [xM,yM]],
]

## Calling and usage convention 3

A list containing coordinate pair lists where each list pair represents an edge connecting two nodes.

Example:

    import pyladder.pyladder as pylad

    ladder_edge_list = [[10,20], [10,30], [10,40], [10,50], [20,30], [20,40], [20,50], [30,40], [40,50]]
    
    my_ladder = pylad.Pyladder()

    if my_ladder.display_graph_plot_edges('edge list example', 'ladder step', ladder_edge_list, True):
        print("Ladder is planar")
    else:
        print("Ladder is not planar")

The call to display_graph_plot_edges will return true or false according to the ladder planarity, and display as follow (see pyladder_edge_list_example.py):

<p align="center">
  <img alt="VS Code in action" src="https://i.postimg.cc/HxWw9Nk4/pyladder-edge-list-example.png">
</p>

### Refer to pyladder_client_dict.py, pyladder_client.py, pyladder_edge_list_examply.py and pyladder_client_file.py for usage examples

## A note on the *.DAT files

The *DAT files were the input files to the original 'C' command line program.  Format used is one node identifier per line.  The first node is the 'source', and every node after and up to '0' are the nodes to which the source connects.

Example:

10
20
25
40
0
20
39
0
...

The sample client file pyladder_client_file.py can be used to injest and parse the *.DAT files into the dictionary data structure format required by pyladder.py, as described in calling convention 1 and the ladder_input dictionary specifically.

## Non-planar samples

The following files are examples of non-planar ladders:
LINK2.DAT
LINK4.DAT
LINK10.DAT
LINK18.DAT

## Issue log

1;  The label for the top 'rung' is not displayed in the matplotlib line plot.  Status = Fixed
2;  The ladder representation in file LINK32.DAT is returning a 'graph rendering failed' message.   Status = Fixed
3;  Improve the visual rendering by including a marker on the vertical line segments for each level of the ladder.  This would be helpful when using the class to render PLC ladder logic.  Status = Oustanding
4;  Comment out debug lines.  Presently the command line output is very verbose.  Status = Fixed
5;  File LINK36.DAT is not rendering correctly (out of order along y-axis).  Status = Fixed
6;  File LINK20.DAT is not rendering correctly (out of order along y-axis).  Status = Fixed
7;  File LINK30.DAT is not rendering correctly.  Status = Fixed, however the ladder is too large to display, must find a scrollable plotting tool.
8;  Implement a scrollable visual plotting library.  Status = Outstanding
9;  Implement a non-visual method call that returns only a planar/non-planar boolean.  Can be used for batch jobs.
10; Transition this issue log to github issues.
11; Plot titles not appearing.  Status = Fixed.
12; Add boolean to planarity check to enable or disable visual display of ladder.  Status = Complete.
13; Visual display of non-planar ladders is no longer generated.  Only False is returned.  Status = Complete.
