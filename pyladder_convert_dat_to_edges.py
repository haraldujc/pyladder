
import sys
from pathlib import Path

# python pyladder_convert_dat_to_edges.py dat_to_edge_conversions.txt
# Ingests the *.DAT files and outputs each as an edge list

# Example, LINK1.DAT:
# 10
# 20
# 30
# 40
# 50
# 0
# 20
# 30
# 40
# 50
# 0
# 30 
# 40
# 0
# 40
# 50
# 0
# will be retuned as follows:
# [[10,20], [10,30], [10,40], [10,50], [20,30], [20,40], [20,50], [30,40], [40,50]]

str_file_list = ['LINK1.DAT','LINK10.DAT','LINK11.DAT','LINK12.DAT','LINK13.DAT','LINK14.DAT','LINK15.DAT','LINK16.DAT','LINK17.DAT','LINK18.DAT','LINK19.DAT','LINK2.DAT','LINK20.DAT','LINK21.DAT','LINK22.DAT','LINK23.DAT','LINK24.DAT','LINK25.DAT','LINK26.DAT','LINK27.DAT','LINK28.DAT','LINK29.DAT','LINK3.DAT','LINK30.DAT','LINK31.DAT','LINK32.DAT','LINK33.DAT','LINK34.DAT','LINK3.DAT','LINK36.DAT','LINK4.DAT','LINK5.DAT','LINK6.DAT','LINK7.DAT','LINK8.DAT','LINK9.DAT']
str_folder = 'test files/'

for str_dat_file in str_file_list:

    edge_list = []
    edge_pair = []

    str_file = Path(str_folder + str_dat_file)
    if str_file.is_file():
        with open(str_file) as file_object:
            for from_edge in file_object:
                edge_pair = []
                for to_edge in file_object:
                    if 0 != int(to_edge):
                        edge_pair.append(int(from_edge))
                        edge_pair.append(int(to_edge))
                        edge_list.append(edge_pair)
                        edge_pair = []
                    else:
                        break

        file_object.close()

        print(str_dat_file, ":" ,edge_list)
    else:
        print('file not found: ' + str_folder + str_dat_file)


