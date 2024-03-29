
# This is a sample client calling the graph rendering engine.
# It constructs two lists
# The first list represents a node and its connections to other nodes
# i.e. [x, y, z, ...] where x is the subject node and y, z, ... are the nodes to which it connects
# This list is passed to the rendering engine
#
# The second list is metadata about the first list, and is used only by matplotlib
# ['node description 1', 'node description 2', 'node description 3',...] where 'node description 1 mapes to 'x' in the first list

import numpy as np
import matplotlib.pyplot as plt
# from pyladder import Pyladder
# from works, added here as an alternative method to use pyladder
import pyladder as pylad

# ladder_input = [[10,20,30,40,50], [20,30,40,50],[30,40],[40,50],[50]]
# ladder_step_labels = ['Part A','Part B','Part C','Part D', 'Finish']

# Another planar example
ladder_input = [[10,20],[20,30,30,40],[30,60,40],[40,50,50,60],[50,60],[60,70,80,110,120],[70,100],[80,100],[100,110],[110,200,150,150,160,160,170,170,180,180,190,190],[120,130,130,140,140],[130,200],[140,200],[150,200],[160,200],[170,200],[180,200],[190,200]]
ladder_step_labels = ['Part A','Part B','Part C','Part D', 'Part E', 'Part F', 'Part G', 'Part H', 'Part I', 'Part J', 'Part K', 'Part L', 'Part M', 'Part N', 'Part O', 'Part P', 'Part Q', 'Part R','Finish']

# Non-planar graph example...
# ladder_input = [[10,20,90,120],[20,30, 100],[30, 40, 120],[40,50,80,90],[50,60,120],[60,70,100],[70,80]]
# ladder_step_labels = ['Part A','Part B','Part C','Part D', 'Part E', 'Part F', 'Part G', 'Finish']

my_ladder = pylad.Pyladder()
if my_ladder.gen_graph(ladder_input):

    print("Ladder is planar")
    # Get the list of line segments as coordinates pairs...
    coors = my_ladder.get_render()

    # Remove horizontal axis labels since it really doesn't have a context
    plt.xticks([])

    # The vertical axis represent the nodes.  Supply an appropriate label here...
    plt.ylabel('ladder step')

    # Plot line segments as per the coors list
    yTicks = []
    for coor in coors:
        plt.plot([coor[0][0],coor[1][0]], [coor[0][1],coor[1][1]], '-o', color='red')
        for node in yTicks:
            if node == coor[0][1]:
                yTicks.remove(node)
                break
        yTicks.append(coor[0][1])

    # Note that this is partial implementation.  Plotting coors for ladders that have 'downward' paths will result in an incorrect plot.
    # Refer to method display_graph_plot for a complete and correct code to render of *.DAT files such as LINK20.DAT

    yTicks.sort()
    # Set the vertical axis labels and display...
    plt.yticks(yTicks, ladder_step_labels)
    plt.title('list of list with external labels list example')
    plt.show()
else:
    print("Ladder is not planer")

