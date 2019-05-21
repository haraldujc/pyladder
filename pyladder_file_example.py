import sys
from pathlib import Path
from pyladder import Pyladder

node_list = []

# -----------------------------------------------------------------------
# This code block dumps the contents of the input files to the ternminal and is for DEBUG purposes only
# str_File_Prefix = 'LINK'
# str_File_Extension = '.DAT'
# str_File_Name = ''
# for i in range(1,36):
#     str_File_Name = str_File_Prefix + str(i) + str_File_Extension
#     print(str_File_Name)
#     with open(str_File_Name) as file_object:
#         for line in file_object:
#             print(line)
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# CALL METHOD 1(comment out the other CALL METHODS if using this one)
# This dictionary will contain the graph nodes
# The key-value pair is
# key = a string label identifying the node
# value = a list of nodes to which this code connects.  The first element of each list is the nodes key, and the subsequent items are the keys of the
# nodes to which this node connects
# Example : # graph_input_sample = {'Part 10' : [10,20,30,40,50], 'Part 20' : [20,30,40,50], 'Part 30' : [30,40], 'Part 40' : [40,50], 'Finish' : [50]}

graph_input_sample = {}
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# CALL METHOD 2 (comment out the other CALL METHODS if using this one)
# Use this code when passing in the file name from the command line
# print ('Number of arguments:' + str(len(sys.argv)) + ' arguments.')
# print ('Argument List: ' + str(sys.argv))

# if len(sys.argv) < 2:
#     str_File_Name = input("File Name? ")
#     print(str_File_Name)
# else:
#     str_File_Name = sys.argv[1]
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# CALL METHOD 3 (comment out the other CALL METHODS if using this one)
# Use this code when needing a hard-coded file name, usually to ease debugging
str_File_Name = 'LINK29.DAT'
# -----------------------------------------------------------------------

max_node = 0

input_file_path = Path(str_File_Name)
if input_file_path.is_file():
    print('Found file ' + str_File_Name)

    with open(str_File_Name) as file_object:
        for line in file_object:
            if len(line) > 0:
                if 0 == int(line):
                    # node_list.append(int(line))
                    graph_input_sample['Part ' + str(node_list[0])] = node_list
                    node_list = []
                else:
                    node_list.append(int(line))
                    max_node = max(int(line), max_node)
    file_object.close()

    node_list = [max_node]
    graph_input_sample['Finish ' + str(node_list[0])] = node_list

    print(graph_input_sample)

    my_graph = Pyladder()
    my_graph.display_graph_plot('Nodes', graph_input_sample)
else:
    print('File ' + str_File_Name + ' does not exist')







