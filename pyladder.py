
import numpy as np
import matplotlib.pyplot as plt

# graph_input_sample = [[10,20,30,40,777,0], [20,30,40,777,0],[30,40,0],[40,777,0]]
# Don't require the 0 marker to denote end of links for each vertex.  The C program used files as input
# and required an upper bound on a link set.  We are using numpy arrays which are explicitly upper bounded.
# Input 1 : Works
# graph_input_sample = [[10,20,30,40,777], [20,30,40,777],[30,40],[40,777]]
# returned dataset:
# 14 Vertical links:
# 0, 10, 777
# 1, 10, 40
# 1, 40, 777
# 2, 10, 30
# 2, 30, 40
# 3, 10, 20
# 3, 20, 30
# 4, 20, 40
# 5, 20, 777
# Horizontal links:
# 10, 0, 3
# 20, 3, 5
# 30, 2, 3
# 40, 1, 4
# 777, 0, 5

# Reference https://en.wikipedia.org/wiki/Planarity_testing

# Input 2 : Non planar
# graph_input_sample = [[10,20,90,777],[20,30, 100],[30, 40, 777],[40,50,80,90],[50,60,777],[60,70,100],[70,80]]

class Pyladder():
    def __init__(self):
        self.ARC = 1
        self.FROND = 2
        self.LEFT, self.RIGHT = 1,2
        self.UP, self.DOWN = 1, 2
        self.VMAX = 70
        self.LMAX = 100
        self.PMAX = 40
        self.n = 0                                                  # Used for numbering the vertices
        self.s = 0                                                  # Number of first vertex in a path

        #self.number = np.array([0] * self.VMAX)                     # Internal vertex numbers
        self.number = np.zeros(self.VMAX, dtype=int)

        self.n_verts = 0                                            # Total number of vertices
        #self.verts = np.array([[0] * 4] * self.VMAX)
        self.verts = np.zeros((self.VMAX, 4), dtype=int)

        self.n_links = 0                                            # Total number of links
        #self.links = np.array([[0] * 4] * self.LMAX)
        self.links = np.zeros((self.LMAX, 4), dtype=int)

        #self.low_1 = np.array([0] * self.VMAX)                      # Lowest vertex reachable
        self.low_1 = np.zeros(self.VMAX, dtype=int)

        #self.low_2 = np.array([0] * self.VMAX)                      # Second lowest vertex reachable
        self.low_2 = np.zeros(self.VMAX, dtype=int)

        self.n_paths = 0                                            # Total number of paths
        #self.path_sizes = np.array([0] * self.PMAX)                 # Sizes of paths
        self.path_sizes = np.zeros(self.PMAX, dtype=int)

        #self.paths = np.array([[0] * self.LMAX] * self.PMAX)
        self.paths = np.zeros((self.PMAX, self.LMAX), dtype=int)

        #self.used = np.array([0] * self.LMAX)                       # Used to keep track of links scanned
        self.used = np.zeros(self.LMAX, dtype=int)

        #self.first_path = np.array([0] * self.VMAX)                 # Number of first path containing vertex
        self.first_path = np.zeros(self.VMAX, dtype=int)

        #self.sides = np.array([[0] * 3] * self.PMAX)
        self.sides = np.zeros((self.PMAX, 3), dtype=int)

        #self.sort_verts= np.array([0] * self.VMAX)                  # Vertices as ordered by paths procedure
        self.sort_verts = np.zeros(self.VMAX, dtype=int)

        self.n_edges = 0                                            # Total number of links with multiples
        #self.edges = np.array([[0] * 2] * self.LMAX)
        self.edges = np.zeros((self.LMAX, 2), dtype=int)

        #self.edge_paths = np.array([0] * self.LMAX)                 # Path number of links
        self.edge_paths = np.zeros(self.LMAX, dtype=int)

        #self.direcs = np.array([0] * self.LMAX)                     # Directions of links (up or down)
        self.direcs = np.zeros(self.LMAX, dtype=int)

        #self.edge_sides = np.array([0] * self.LMAX)                 # Sides of links (left or right)
        self.edge_sides = np.zeros(self.LMAX, dtype=int)

        #self.parents = np.array([0] * self.LMAX)                    # Parent paths of links
        self.parents = np.zeros(self.LMAX, dtype=int)

        #self.columns = np.array([0] * self.LMAX)                    # Column numbers of links
        self.columns = np.zeros(self.LMAX, dtype=int)

        # self.matrix = np.array([[0] * self.LMAX] * self.VMAX)
        self.first_path[0] = 1
        self.debug = False

    # This method takes a string label for the y-xis plot, and a dictionary of keys representing the node name
    # used for the y-axis and corresponding values which is a list of integer coordinates representing line segments connecting nodes as follows:
    # [[x1,y1],[x1, y2],[x3, y3],...,[.,.]]
    # The method then proceeds to render a visual representation of the graph, whether it is planar or not.
    # If the graph is planar, true is returned, false is not
    def display_graph_plot_edges(self, ladder_title, y_axis_label, graph_def_edges):
        ladder_input = {}
        last_node = -1

        for edge in graph_def_edges:
            if 2 == len(edge):
                temp = []
                if str(edge[0]) in ladder_input:
                    temp = ladder_input[str(edge[0])]
                    temp.append(edge[1])
                    ladder_input[str(edge[0])] = temp
                else:
                    temp.append(edge[0])
                    temp.append(edge[1])
                    ladder_input[str(edge[0])] = temp
                if edge[1] > last_node:
                    last_node = edge[1]

        ladder_input[str(last_node)] = [last_node]
        return(self.display_graph_plot(ladder_title, y_axis_label, ladder_input))

    # This method takes a string label for the y-xis plot, and a dictionary of keys representing the node name
    # used for the y-axis and corresponding values which is a dictionary of coordinate lists for the connecting line segments, as follows:
    # {'node x1' : [node x1, connection to node x2, connection to node x3, connection to node x4, ...], 'node x2' : [connection to node x3, ...]}
    # The method then proceeds to render a visual representation of the graph, whether it is planar or not.
    # If the graph is not planar, an advisory message is generated.
    def display_graph_plot(self, ladder_title, y_axis_label, graph_def):
        graph_lst = []
        graph_labels = []
        yTicks = []

        for key, value in graph_def.items():
            graph_lst.append(value)

        if self.gen_graph(graph_lst):

            # Get the list of line segments as coordinates pairs...
            # Some ladders have paths that retreat which will render incorrectly by matplotlib graph
            coors = self.get_render()

            # Create y coordinate translation dictionary
            y_dict = {}
            y = 10
            for i in range(0, self.n_verts):
                y_dict[self.verts[i][0]] = y 
                yTicks.append(y)
                for key, value in graph_def.items():
                    if value[0] == self.verts[i][0]:
                        graph_labels.append(key)
                y = y + 10

            # Remove horizontal axis labels since it doesn't have a context
            plt.xticks([])
            plt.suptitle = ladder_title
            plt.ylabel(y_axis_label)

            # Plot line segments as per the coors list
            for coor in coors:
                plt.plot([coor[0][0], coor[1][0]], [y_dict[coor[0][1]], y_dict[coor[1][1]]], '-o', color='red')

            # Set the vertical axis labels and display...
            plt.yticks(yTicks, graph_labels)
            plt.show()
            return True
        else:
            return False

    # This method is a silent version of display_graph_plot.  It accepts a list of node lists as follows:
    # [[x1, x2, x3, x4,...],[x2, x3, x4, ...],[...],...] 
    # The first element of each sub-list is the node, and each subsequent list member is the nodes to which the first element connects.
    # 
    def gen_graph(self, graph_def):
        bln_fail = False
        if self.get_links(graph_def):
            # debug self.disp_links(1)
            self.search(self.verts[0][0], 0)
            self.sort()
            # debug self.disp_links(2)
            self.s = 0
            if self.path_finder(self.verts[0][0]):
                self.scan_paths()
                # debug self.disp_links(3)
                if self.convert_links():
                    # debug self.disp_links(4)
                    bln_fail = not self.scan_links(1) ## debug
                    # debug self.disp_links(5)
                    if bln_fail:
                        bln_fail = not self.scan_links(-1)
                        # debbug self.disp_links(6)
                        if bln_fail:
                            self.re_order()
                            # debug self.disp_links(7)
                            bln_fail = not self.scan_links(1)
                            # debug self.disp_links(8)

                    if not bln_fail:
                        # debug self.disp_links(9)
                        self.adjust_links()
                        # debug self.disp_links(10)
                        self.sort_links()
                        # debug self.disp_links(11)
                        self.multi_links()
                        # debug self.disp_links(12)
                        self.adjust_columns()
                        # debug self.disp_links(13)
                        self.sort_links()
                        # debug self.disp_links(14)
                        # debug self.disp_graph()

        return not bln_fail

    #  This method writes the tables of vertical and horizontal links to   
    #  the output file.                                                        
    def disp_links(self, iStep):
        print(str(iStep) + " Vertical links:")
        for i in range(0, self.n_edges):
            print(str(self.columns[i]) + ", " + str(self.edges[i][0]) + ", " + str(self.edges[i][1]))
        print("Horizontal links:")
        for i in range(0, self.n_verts):
            print(str(self.verts[i][0]) + ", " + str(self.verts[i][2]) + ", " + str(self.verts[i][3]))
        # debug print("Edge sides:")
        # debug for i in range(0, self.n_verts):
        # debug    print(str(self.edge_sides[i]))
        return

    # This method should be called after gen_graph and returns a list of line segments which can be used to
    # plot the graph by any data visualization library.  The data structure format is:
    # [[x1, y1],[x2, y2]
    # [x3, y3],[x4, y4],
    # [x5, y5],[x6, y6], 
    # ...]
    def get_render(self):
        coor = []
        for i in range(0, self.n_edges):
            coor.append( [[self.columns[i], self.edges[i][0]], [self.columns[i], self.edges[i][1]]] )
        for i in range(0, self.n_verts):
            coor.append( [[self.verts[i][2], self.verts[i][0]], [self.verts[i][3], self.verts[i][0]]] )
        return coor

    #  This method reads the ladder data from the input list. It stores    
    #  the vertices in ascending numerical order in the array verts (column 0) 
    #  and the links in the array links (column 0 for first vertex, column 1   
    #  for second vertex and column 3 for multiplicity of link). It also adds  
    #  the extra vertex and links.                                             
    #  The method returns FALSE if the input list contains invalid data or 
    #  the maximum number of links or vertices is exceeded. It returns TRUE    
    #  otherwise.                                                              
    def get_links(self, graph_def):
        self.n_verts = 1
        self.n_links = 2
        self.verts[0][0] = 0
        fail_ret = False
        is_vertex = False

        for i in range(0,2):
            self.links[i][0] = 0
            self.links[i][2] = 0
            self.links[i][3] = 1

        for self.node_links in graph_def:

            is_vertex = True

            if fail_ret or self.n_links >= self.LMAX:
                fail_ret = True
                break

            # print(self.node_links) # debug
            fail_ret = not self.add_vert(self.node_links[0])
            w = 0
            
            for node in self.node_links:
                if not is_vertex:
                    # print(node) # debug
                    is_vertex = False

                    if fail_ret:
                        break

                    if node == w:
                        self.links[self.n_links - 1][3] += 1
                    else:
                        w = node
                        self.links[self.n_links][0] = self.node_links[0]
                        self.links[self.n_links][1] = node
                        self.links[self.n_links][2] = 0
                        self.links[self.n_links][3] = 1
                        self.n_links += 1
                        fail_ret = not self.add_vert(node)
                else:
                    is_vertex = False

        if fail_ret:
            if self.n_links >= self.LMAX:
                print("Maximum number of links exceeded\n")
            else:
                print("Invalid data in input stream\n")
        
        if not fail_ret:
            self.links[0][1] = self.verts[1][0]
            self.links[1][1] = self.verts[self.n_verts - 1][0]

        return not fail_ret

    #  This method checks whether a vertex is already in the array verts,  
    #  and adds it to the array if needed.                                     
    #  v is the vertex to be checked.                                          
    #  The method returns FALSE if the maximum number of vertices is       
    #  exceeded. It returns TRUE otherwise.                                    
    def add_vert(self, v):
        i = 0
        # print('i = ' + str(i)) # debug
        # print(self.verts)
        # print(self.n_verts)
        # print(self.verts[i][0])

        while i < self.n_verts and v > self.verts[i][0]:
            i += 1
        if v != self.verts[i][0]:
            if self.n_verts < self.VMAX:

                j = self.n_verts

                while j > i:
                    self.verts[j][0] = self.verts[j-1][0]
                    j -= 1

                self.verts[i][0] = v
                self.n_verts += 1
                return True
            else:
                print("Maximum number of vertices exceeded\n")
                return False
        else:
            return True


    #  This method switches the two vertices of a link in order to have    
    #  them in the order accessed when scanning through the graph.             
    #  i is the index of the link in array links.                              
    def switch_link(self, i):
        self.links[i][0], self.links[i][1] = self.links[i][1], self.links[i][0]

    #  This method checks the element i in the array links. If one of the  
    #  vertices is equal to the specified vertex v, it returns the other ver-  
    #  tex as w and the value TRUE, otherwise it returns the value FALSE.      
    #  i is the index of the link to be checked.                               
    #  v is the vertex to be looked for.                                       
    #  w is the other vertex in the link (if found).                           
    #  The method returns TRUE if v is found in the link and FALSE other-  
    #  wise.                                                                   
    def find_link(self, i, v):
        w = -1
        if self.links[i][0] == v:
            w = self.links[i][1]
        if (self.links[i][1] == v):
            w = self.links[i][0]

        return w 

    #  This method is called recursively in order to scan through the      
    #  graph, number each vertex (in array number), mark each vertex as an     
    #  "arc" or a "frond" (in column 2 of array verts), and find for each      
    #  vertex the lowest numbered vertex reachable from it (in array low_1)    
    #  and the second lowest numbered vertex reachable from it (in array       
    #  low_2).                                                                 
    #  v is the vertex from which to start the scan.                           
    #  u is the vertex from which v was reached.                               
    def search(self, v, u):
        w, i, i_v, i_w = 0,0,0,0

        self.n += 1
        i_v = self.n_vert(v)
        self.number[i_v] = self.n
        self.low_1[i_v] = self.n
        self.low_2[i_v] = self.n

        i = 0
        while i < self.n_links:
            w = self.find_link(i, v)
            if w >= 0:
                i_w = self.n_vert(w)
                if 0 == self.number[i_w]:
                    self.links[i][2] = self.ARC
                    if w == self.links[i][0]:
                        self.switch_link(i)
                    self.search(w, v)
                    if self.low_1[i_w] < self.low_1[i_v]:
                        self.low_2[i_v] = min([self.low_1[i_v], self.low_2[i_w]])
                        self.low_1[i_v] = self.low_1[i_w]
                    else:
                        if self.low_1[i_w] == self.low_1[i_v]:
                            self.low_2[i_v] = min([self.low_2[i_v], self.low_2[i_w]])
                        else:
                            self.low_2[i_v] = min([self.low_2[i_v], self.low_1[i_w]])
                else:
                    if self.number[i_w] < self.number[i_v] and w != u:
                        self.links[i][2] = self.FROND
                        if w == self.links[i][0]:
                            self.switch_link(i)
                        if self.number[i_w] < self.low_1[i_v]:
                            self.low_2[i_v] = self.low_1[i_v]
                            self.low_1[i_v] = self.number[i_w]
                        else:
                            if self.number[i_w] > self.low_1[i_v]:
                                self.low_2[i_v] = min([self.low_2[i_v], self.number[i_w]])
            i += 1

        return

    #  This method finds the index of a given vertex in the array verts.   
    #  v is the vertex to be checked.                                          
    #  The method returns the index of the vertex in the array verts.      
    def n_vert(self, v):
        i = 0
        while i < self.n_verts  and self.verts[i][0] != v:
            i += 1

        return i


    #  This method checks whether the current link crosses any horizontal  
    #  links.                                                                  
    #  i is the index of the current link.                                     
    #  inc is the increment value (1 or -1).                                   
    #  The method returns TRUE if the current link crosses any horizontal  
    #  links and FALSE otherwise.                                              
    def crossover(self, i, inc):
        cross = False
        edge_1 = self.n_vert(self.edges[i][0])
        edge_2 = self.n_vert(self.edges[i][1])
        i_min = min([edge_1, edge_2])
        i_max = max([edge_1, edge_2])
        for j in range(i_min + 1, i_max):
            if -1 == inc:
                if self.columns[i] > self.verts[j][2] and self.columns[i] <= self.verts[j][3]:
                    cross = True
                    break
            else:
                if self.columns[i] >= self.verts[j][2] and self.columns[i] < self.verts[j][3]:
                    cross = True
                    break


        return cross


    #  This method checks whether the current link overlaps any other      
    #  links.                                                                  
    #  i is the index of the current link.                                     
    #  The method returns TRUE if the current link overlaps any other      
    #  links and FALSE otherwise.                                              
    def overlap(self, i):
        edge_1 = self.n_vert(self.edges[i][0])
        edge_2 = self.n_vert(self.edges[i][1])
        i_min = min([edge_1, edge_2])
        i_max = max([edge_1, edge_2])
        move = False
        for j in range(0, i):
            if (self.columns[i] == self.columns[j]) and (self.edges[i][0] != self.edges[j][0] or self.edges[i][1] != self.edges[j][1]):
                edge_1 = self.n_vert(self.edges[j][0])
                edge_2 = self.n_vert(self.edges[j][1])
                j_min = min([edge_1, edge_2])
                j_max = max([edge_1, edge_2])
                if not (i_max <= j_min or j_max <= i_min):
                    move = True
                    break

        return move

    #  This method adjusts the columns of all the links to the left or    
    #  right of the current link when inc is equal to -1 or 1 respectively.   
    #  It also updates the column ranges for the vertices (the horizontal     
    #  links).                                                                
    #  i is the index of the current link.                                     
    #  inc is the increment value (1 or -1).                                   
    def move_columns(self, i, inc):
        for j in range(0, i):
            if (inc == -1 and self.columns[j] <= self.columns[i]) or (inc == 1 and self.columns[j] >= self.columns[i]):
                self.columns[j] += inc
        for j in range (0, self.n_verts):
            if True == self.verts[j][1]:
                for k in range(2, 4):
                    if (inc == -1 and self.verts[j][k] <= self.columns[i]) or (inc == 1 and self.verts[j][k] >= self.columns[i]):
                        self.verts[j][k] += inc


    #  This method updates the columns range for a given vertex.           
    #  i is the index of the vertex.                                           
    #  column is the column number to be used.                                 
    def update_vert(self, i, column):
        if False == self.verts[i][1]:
            self.verts[i][1] = True
            self.verts[i][2] = column
            self.verts[i][3] = column
        else:
            self.verts[i][2] = min([self.verts[i][2], column])
            self.verts[i][3] = max([self.verts[i][3], column])
            
    #  This method checks whether any links cross each other.              
    #  The method returns FALSE if any links cross each other. It returns  
    #  TRUE otherwise.                                                         
    def check_links(self):
        vert, edge_1, edge_2, temp_1, temp_2 = 0,0,0,0,0
        fail = False

        for i in range(0, self.n_verts):
            if fail:
                break
            vert = self.n_vert(self.verts[i][0])
            for j in range(0, self.n_edges):
                temp_1 = self.n_vert(self.edges[j][0])
                temp_2 = self.n_vert(self.edges[j][1])
                edge_1 = min([temp_1, temp_2])
                edge_2 = max([temp_1, temp_2])
                if edge_1 < vert and vert < edge_2 and self.verts[i][2] < self.columns[j] and self.columns[j] < self.verts[i][3]:
                    fail = True
                    break
        return not fail

    #  This method sets up the arrays verts and direcs for the order of    
    #  vertices established in the path generating procedure. It is called if  
    #  the ladder could not be formed with the vertices in ascending numerical 
    #  order.                                                                  
    def re_order(self):
        for i in range(0, self.n_verts):
            self.verts[i][0] = self.sort_verts[i]
        for i in range(0, self.n_edges):
            if self.n_vert(self.edges[i][0]) < self.n_vert(self.edges[i][1]):
                self.direcs[i] = self.UP
            else:
                self.direcs[i] = self.DOWN

    #  This method scans through the links (sorted according to the paths) 
    #  in order to form the ladder. The columns of the links are stored in the 
    #  array columns. The leftmost and rightmost columns used by links with    
    #  a given vertex are stored in columns 2 and 3 of the array verts. Column 
    #  1 of the array verts is used for keeping track of the vertices acces-   
    #  sed. The columns range for a vertex is termed a horizontal link.        
    #  The column of the first link is set to 0. When a new link in the same   
    #  path is processed the column is set to the same column as the previous  
    #  link and the increment inc is set according to the input parameter      
    #  side. When the first link in a new path is processed the column is set  
    #  according to the column range of the vertex from where the path starts, 
    #  the sides and directions of the links involved, and the other paths     
    #  starting from this link which are already processed. The increment inc  
    #  is set according to the direction of the parent path at the vertex      
    #  where the new path starts and the side of the new path. Multiple links  
    #  are assigned the same column. They will be separated later.             
    #  The columns of the new link and the previous links are then adjusted in 
    #  order to prevent links from overlapping or crossing each other, and     
    #  finally the column ranges of the link's vertices are updated.           
    #  side is the increment to be used within a path (if it changes direction 
    #  or is blocked by previous links) and can be 1 or -1.                    
    #  The method returns FALSE if the forming of the ladder fails due to  
    #  links crossing each other. It returns TRUE otherwise.                   
    def scan_links(self, side):
        #first_lcl = np.array([0] * self.LMAX)
        first_lcl = np.zeros(self.LMAX, dtype=int)
        fail_ret = False
        inc = 1
        i_start, i_end = 0, 0

        for i in range(0, self.n_verts):
            self.verts[i][1] = False
            self.verts[i][2] = 0
            self.verts[i][3] = 0

        for i in range(0, self.n_links):
            self.columns[i] = 0

        first_lcl[self.edge_paths[0] - 1] = 0

        for i in range(0, self.n_edges):
            #debug self.disp_links(700+i)
            if fail_ret:
                break
            if i > 0:
                if self.edge_paths[i - 1] == self.edge_paths[i]:
                    self.columns[i] = self.columns[i - 1]
                    if self.direcs[i - 1] != self.direcs[i]:
                        if self.LEFT == self.edge_sides[i]:
                            inc = -1 * side
                        else:
                            inc = side
                else:
                    first_lcl[self.edge_paths[i] - 1] = i
                    i_start = first_lcl[self.parents[i] - 1]
                    i_end = first_lcl[self.parents[i]]
                    j = i_start
                    # debug self.disp_links(898)

                    while j < i_end and self.edges[i][0] != self.edges[j][1]:
                        j += 1

                    if (self.edge_sides[i] == self.LEFT and self.direcs[j] == self.UP) or (self.edge_sides[i] == self.RIGHT and self.direcs[j] == self.DOWN):
                        inc = -1
                    else:
                        inc = 1
                    # debug self.disp_links(899)
                    if j < i_end and self.direcs[j] == self.direcs[j + 1]:
                        if -1 == inc:
                            self.columns[i] = min([self.columns[j],self.columns[j + 1]])
                        else:
                            self.columns[i] = max([self.columns[j],self.columns[j + 1]])
                    else:
                        self.columns[i] = self.columns[j]
                    
                    # debug self.disp_links(900)
                    if self.direcs[i] == self.direcs[j]:
                        for j in range(0, i):
                            if self.edges[i][0] == self.edges[j][0] and self.edge_sides[i] == self.edge_sides[j] and self.parents[i] == self.parents[j]:
                                if self.direcs[i] == self.direcs[j]:
                                    if -1 == inc:
                                        self.columns[i] = min([self.columns[i], self.columns[j]])
                                    else:
                                        self.columns[i] = max([self.columns[i], self.columns[j]])
                                else:
                                    fail_ret = True
                                    break

            # debug self.disp_links(901)
            if i > 0:
                fail_ret = not self.move_links(i, inc)
            # debug self.disp_links(902)
            if not fail_ret:
                j = self.n_vert(self.edges[i][0])
                self.update_vert(j, self.columns[i])
                # debug self.disp_links(903)
                j = self.n_vert(self.edges[i][1])
                self.update_vert(j, self.columns[i])
            # debug self.disp_links(904)

        if not fail_ret:
            fail_ret = not self.check_links()

        # debug self.disp_links(902)

        return not fail_ret

    #  This method moves the previous links and/or the current link so     
    #  that no links will overlap or cross each other. If the current link is  
    #  in the same path as the previous link, the previous links are moved in  
    #  order to accommodate the current link if needed. Then the column of the 
    #  current link is adjusted until it does not cross any horizontal links,  
    #  and finally the column of the current link and the previous links are   
    #  adjusted so that links will not overlap each other.                     
    #  If the current link is the last link in the path (the "frond"), and its 
    #  column is outside the current columns range for its second vertex, then 
    #  the method checks for other links crossing in between. If a cros-   
    #  sing link is found on the left or right of the current link with inc    
    #  equal to -1 or 1 respectively, then the column of the current link is   
    #  set beyond the crossing link, and the method calls itself recur-    
    #  sively in order to repeat the links adjustment procedure. If the cros-  
    #  sing link is found on the right or left with inc equal to -1 or 1 res-  
    #  pectively, then the forming of the ladder has failed.                   
    #  i is the index of the current link.                                     
    #  inc is the increment value (1 or -1).                                   
    #  The method returns FALSE if the forming of the ladder fails due to  
    #  links crossing each other. It returns TRUE otherwise.                   
    def move_links(self, i, inc):
        edge_1, edge_2, k_min, k_max, cross, stop, move, fail_ret = 0, 0, 0, 0, 0, 0, 0, False

        if (self.edge_paths[i - 1] == self.edge_paths[i]):
            self.columns[i] -= inc
            move = not self.crossover(i, inc)
            self.columns[i] += inc
            stop = not self.crossover(i, inc)
            if move and not stop:
                self.move_columns(i, inc)
        else:
            stop = False

        while not stop:
            stop = not self.crossover(i, inc)
            if not stop:
                self.columns[i] += inc

        move = self.overlap(i)

        if move:
            self.columns[i] += inc
            move = self.overlap(i)
            if move:
                self.move_columns(i, inc)

        j = self.n_vert(self.edges[i][1])

        if self.verts[j][1] == True and (self.columns[i] < self.verts[j][2] or self.columns[i] > self.verts[j][3]):
            cross = False
            for k in range(0, i):
                if (self.columns[i] <= self.columns[k] and self.columns[k] <= self.verts[j][2]) or (self.verts[j][3] <= self.columns[k] and self.columns[k] <= self.columns[i]):
                    edge_1 = self.n_vert(self.edges[k][0])
                    edge_2 = self.n_vert(self.edges[k][1])
                    k_min = min([edge_1, edge_2])
                    k_max = max([edge_1, edge_2])

                    if k_min < j and k_max > j:
                        cross = True
                        break
            if cross:
                if (-1 == inc and self.columns[i] < self.verts[j][2]) or (1 == inc and self.columns[i] > self.verts[j][3]):
                    fail_ret = True
                else:
                    self.columns[i] = self.columns[k] + inc
                    fail_ret = not self.move_links(i, inc)

        return not fail_ret



    #  This method returns the index of a vertex with internal number n_v  
    #  in the array numbers.                                                   
    #  n_v is the internal number of the vertex to be checked.                 
    #  The method returns the index of n_v in the array numbers.           
    def n_number(self, n_v):
        i = 0
        while i < self.n_verts and n_v != self.number[i]:
            i += 1
        return i

    #  This method assigns each link a number (in array phi) based on its  
    #  vertices, and sorts the links according to these numbers. If two links  
    #  have the same number, they are sorted by the internal numbers of their  
    #  first vertices.                                                         
    def sort(self):
        # phi = np.array([0] * self.LMAX)
        # num = np.array([0] * self.LMAX)

        phi = np.zeros(self.LMAX, dtype=int)
        num = np.zeros(self.LMAX, dtype=int)

        i_v = 0
        i_w = 0

        # self.links = np.array([[0] * 4] * self.LMAX)
        for i in range(0, self.n_links):
            i_v = self.n_vert(self.links[i][0])
            i_w = self.n_vert(self.links[i][1])
            if self.FROND == self.links[i][2]:
                phi[i] = 2 * self.number[i_w] + 1
            else:
                if self.low_2[i_w] >= self.number[i_v]:
                    phi[i] = 2 * self.low_1[i_w]
                else:
                    phi[i] = 2 * self.low_1[i_w] + 1
            num[i] = self.number[i_v]

        for i in range(self.n_links - 1, 0, -1):
            for j in range(0, i):
                if (phi[j] > phi[j + 1] or (phi[j] == phi[j + 1] and num[j] > num[j + 1])):
                    for k in range(0, 4):
                        self.links[j][k], self.links[j + 1][k] = self.links[j+1][k], self.links[j][k]

                    phi[j], phi[j+1] = phi[j+1], phi[j]
                    num[j], num[j+1] = num[j+1], num[j]



    #  This method is called recursively in order to scan through the      
    #  graph, find the paths, and determine the side of each path with respect 
    #  to the parent path.                                                     
    #  v is the vertex from which to start the scan.                           
    #  The method returns FALSE if the graph is found to be non-planar, or 
    #  the maximum number of paths is exceeded. It returns TRUE otherwise.     
    def path_finder(self, v):
        n_v = self.number[self.n_vert(v)]
        fail_ret = False

        for i in range(0, self.n_links):
            if fail_ret:
                break
            if self.used[i] == False and self.links[i][0] == v:
                w = self.links[i][1]
                n_w = self.number[self.n_vert(w)]
                self.used[i] = True
                if self.links[i][2] == self.ARC:
                    if 0 == self.s:
                        self.s = n_v
                        fail_ret = not self.start_path(n_v)

                    if not fail_ret:
                        self.add_to_path(n_w)
                        self.first_path[n_w - 1] = self.n_paths
                        fail_ret = not self.path_finder(w)
                else:
                    if 0 == self.s:
                        self.s = n_v
                        fail_ret = not self.start_path(n_v)
                    
                    if not fail_ret:
                        self.add_to_path(n_w)
                        self.s = 0
                        fail_ret = not self.update_sides()
                        if fail_ret:
                            # print("Ladder is not planar\n")
                            # self.disp_links
                            fail_ret = False

        return not fail_ret


    #  This method updates the paths data when a new path is started. The  
    #  number of the parent path is stored in array sides, column 1.           
    #  n_v is the internal number of the first vertex of the new path.         
    #  The method returns FALSE if the maximum number of paths is excee-   
    #  ded. It returns TRUE otherwise.                                         
    def start_path(self, n_v):
        fail = False
        if self.n_paths < self.PMAX:
            self.paths[self.n_paths][0] = n_v
            self.path_sizes[self.n_paths] = 1
            if 0 == self.n_paths:
                self.sides[self.n_paths][1] = 0
            else:
                self.sides[self.n_paths][1] = self.first_path[self.s - 1]
            self.n_paths += 1
            fail = False
        else:
            print("Maximum number of paths exceede\n")
            fail = True

        return not fail


    #  This method marks the current path as "left". Then it scans the     
    #  previous paths and swaps their sides if needed, so that no paths will   
    #  cross each other. The swapping is done in two steps. First the paths    
    #  affected by the new path are swapped if needed. Then the paths not      
    #  swapped in this step are checked and swapped if needed. If a path has   
    #  to be swapped for a second time, this means that the graph is non-      
    #  planar. The path sides are stored in column 0 of array sides. Column 2  
    #  of this array is used for keeping track of paths that were swapped.     
    #  The method returns FALSE if the graph is found to be non-planar.    
    #  It returns TRUE otherwise.                                              
    def update_sides(self):
        for i in range(0, self.n_paths - 1):
            self.sides[i][2] = False
        self.sides[self.n_paths - 1][0] = self.LEFT
        self.sides[self.n_paths - 1][2] = True
        fail_ret = not self.swap_sides_1(self.n_paths)
        if not fail_ret:
            for i in range(self.n_paths - 1, 0, -1):
                if fail_ret:
                    break
                if False == self.sides[i - 1][2] :
                    fail_ret = not self.swap_sides_2(i)

        return not fail_ret

    #  This method is called recursively in order to swap the sides of     
    #  paths in the first step. It scans through the paths in descending       
    #  order. If a path crosses the path where the scan starts, it swaps this  
    #  path, and then calls itself to check for lower numbered paths that need 
    #  to be swapped as a result, and so on.                                   
    #  n_path is the number of the path where the scan starts.                 
    #  The method returns FALSE if the graph is found to be non-planar.    
    #  It returns TRUE otherwise.                                              
    def swap_sides_1(self, n_path):
        fail_ret = False
        n_start = self.paths[n_path -1][0]
        n_end = self.paths[n_path - 1][self.path_sizes[n_path - 1] - 1]
        n_side = self.sides[n_path - 1][0]
        n_parent = self.sides[n_path - 1][1]
        for i in range(n_path - 1, 0, -1):
            if fail_ret:
                break
            if (self.check_swap(n_start, n_end, n_side, n_parent, i)):
                fail_ret = not self.swap_element(i)
                if not fail_ret:
                    fail_ret = not self.swap_sides_1(i)
        return not fail_ret

    #  This method is called in order to swap the sides of paths in the    
    #  second step. It scans through the paths in descending order. If a path  
    #  crosses the path where the scan starts, it swaps the path where the     
    #  scan starts, and then swaps other paths that need to be swapped as a    
    #  result.                                                                 
    #  n_path is the number of the path where the scan starts.                 
    #  The method returns FALSE if the graph is found to be non-planar.    
    #  It returns TRUE otherwise.                                              
    def swap_sides_2(self, n_path):
        fail_ret = False
        n_start = self.paths[n_path - 1][0]
        n_end = self.paths[n_path - 1][self.path_sizes[n_path - 1] - 1]
        n_side = self.sides[n_path - 1][0]
        n_parent = self.sides[n_path - 1][1]
        for i in range(n_path - 1, 0, -1):
            if fail_ret:
                break
            if (self.check_swap(n_start, n_end, n_side, n_parent, i)):
                fail_ret = not self.swap_element(n_path)
                n_side = self.sides[n_path - 1][0]
                for j in range(self.n_paths, 0, -1):
                    if fail_ret:
                        break
                    if self.check_swap(n_start, n_end, n_side, n_parent, j):
                        fail_ret = not self.swap_sides_2(j)
        return not fail_ret

    #  This method is called recursively in order to check if a path cros- 
    #  ses other paths. First it checks if the path specified crosses another  
    #  path. If not, it calls itself to check if the path specified crosses    
    #  any of the paths branching out of this path, and so on.                 
    #  n_start is the internal number of the first vertex in the path checked. 
    #  n_end is the internal number of the last vertex in the path checked.    
    #  n_side is the side the path checked (needed when checking another path  
    #  with the same parent path as the path checked), or zero (as not needed  
    #  when checking the paths branching out of this path).                    
    #  n_parent is the number of the parent path. Only paths with this parent  
    #  path need to be checked.                                                
    #  i_path is the number of the path to be checked for crossing, or zero if 
    #  all paths need to be checked for crossing.                              
    #  The method returns TRUE if a crossing is found and FALSE otherwise. 
    def check_swap(self, n_start, n_end, n_side, n_parent, i_path):
        swap = False
        for i in range(1, self.n_paths):
            if swap:
                break
            if (0 == i_path or (i_path == i and self.sides[i - 1][0] == n_side)) and self.sides[i - 1][1] == n_parent:
                i_start = self.paths[i - 1][0]
                i_end = self.paths[i - 1][self.path_sizes[i - 1] - 1]
                if (n_end < i_end and i_end < n_start and n_start < i_start) or (i_end < n_end and n_end < i_start and i_start < n_start):
                    swap = True
                else:
                    swap = self.check_swap(n_start, n_end, 0, i, 0)
        return swap

    #  This method is called recursively in order to swap the sides of a   
    #  path and all the paths branching out of it. First it checks if the path 
    #  specified has already been swapped before. If not, it swaps its side,   
    #  and then calls itself in order to swap the sides of the paths branching 
    #  out of it.                                                              
    #  n_path is the number of the path to be swapped.                         
    #  The method returns FALSE if the path specified or any of the paths  
    #  branching out of it have been swapped before (indicating that the graph 
    #  is non-planar). It returns TRUE otherwise.                              
    def swap_element(self, n_path):

        fail_ret = False

        if True == self.sides[n_path - 1][2]:
            fail_ret = True
        else:
            fail_ret = False
            self.sides[n_path - 1][2] = True
            if self.RIGHT == self.sides[n_path - 1][0]:
                self.sides[n_path - 1][0] = self.LEFT
            else:
                self.sides[n_path - 1][0] = self.RIGHT
            for i in range(1, self.n_paths + 1):
                if self.sides[i - 1][1] == n_path:
                    fail_ret = not self.swap_element(i)
        return not fail_ret

    #  This method scans the paths and sorts the vertices according to the 
    #  order of their appearance there. The vertices in this order are stored  
    #  in the array sort_verts. This order of vertices is used if the program  
    #  fails to produce the ladder with the vertices ordered in ascending nu-  
    #  merical order. If the "-d" switch is specified, the method writes   
    #  the sorted vertices to the output file.                                 
    def scan_paths(self):
        vert, vert_max, count, temp, n, k = 0, 0, 0, 0, 0, 0
        # right_max = np.array([0] * self.PMAX)
        # left_max = np.array([0] * self.PMAX)

        right_max = np.zeros(self.PMAX, dtype=int)
        left_max = np.zeros(self.PMAX, dtype=int)

        for j in range(1, self.path_sizes[0] - 1):
            self.sort_verts[count] = self.verts[self.n_number(self.paths[0][j])][0]
            count += 1
        
        right_max[0] = self.sort_verts[count - 1]
        left_max[0] = self.sort_verts[count - 1]

        for i in range(1, self.n_paths):
            n = self.path_sizes[i]
            if n > 2:
                vert = self.verts[self.n_number(self.paths[i][0])][0]
                k = 0
                while k < count and self.sort_verts[k] != vert:
                    k += 1
                vert_max = max([self.verts[self.n_number(self.paths[i][0])][0], self.verts[self.n_number(self.paths[i][n - 2])][0]])

                if self.LEFT == self.sides[i][0]:
                    left_max[i] = min(left_max[self.sides[i][1] - 1], vert_max)
                    vert_max = left_max[i]
                else:
                    right_max[i] = min([right_max[self.sides[i][1] - 1], vert_max])
                    vert_max = right_max[i]

                temp = self.verts[self.n_number(self.paths[i][1])][0]

                j = count - 1
                if temp > vert and temp <= vert_max:
                    while j > k:
                        self.sort_verts[j + n - 2] = self.sort_verts[j]
                        j -= 1
                    for j in range(1, n - 1):
                        self.sort_verts[k + j] = self.verts[self.n_number(self.paths[i][j])][0]
                else:
                    while j >= k:
                        self.sort_verts[j + n - 2] = self.sort_verts[j]
                        j -= 1
                    for j in range(1, n - 1):
                        self.sort_verts[k + n - j -2] = self.verts[self.n_number(self.paths[i][j])][0]
                count += n - 2
        # if self.debug:
        #     print("Order of vertices:\n")
        #     for i in range(0, count):
        #         print(self.sort_verts[i])
        #     print("\n")




    #  This method adds a new vertex to the current path.                  
    #  n_v is the internal number of the vertex to be added to the path.       
    def add_to_path(self, n_v):
        self.paths[self.n_paths - 1][self.path_sizes[self.n_paths - 1]] = n_v
        self.path_sizes[self.n_paths - 1] += 1


    #  This method stores the links in the order in which they are found   
    #  in the paths. If a link has multiplicity n, it is stored n times. The   
    #  links are stored in the array edges, their paths are stored in the      
    #  array edge_paths, their directions (up/down) are stored in the array    
    #  direcs, their sides (left/right) are stored in the array edge_sides,    
    #  and their parent paths are stored in the array parents. The method  
    #  skips the links with vertex 0 and removes this vertex from the array    
    #  verts.                                                                  
    #  The method returns FALSE if the maximum number of links is excee-   
    #  ded. It returns TRUE otherwise.                                         
    def convert_links(self):
        side, parent, vert_1, vert_2, mult, fail_ret = 0, 0, 0, 0, 0, 0

        self.n_edges = 0
        fail_ret = False

        for i in range(0, self.n_paths):
            if fail_ret:
                break

            side = self.sides[i][0]
            parent = self.sides[i][1]
            vert_2 = self.verts[self.n_number(self.paths[i][0])][0]

            for j in range(1, self.path_sizes[i]):
                vert_1 = vert_2
                vert_2 = self.verts[self.n_number(self.paths[i][j])][0]
                k = 0
                while k < self.n_links and (self.links[k][0] != vert_1 or self.links[k][1] != vert_2):
                    k += 1
                mult = self.links[k][3]
                if vert_1 != 0 and vert_2 != 0:
                    if self.n_edges <= self.LMAX - mult:
                        for k in range(0, mult):
                            if fail_ret:
                                break

                            self.edges[self.n_edges][0] = vert_1
                            self.edges[self.n_edges][1] = vert_2
                            self.edge_paths[self.n_edges] = i + 1
                            if vert_1 < vert_2:
                                self.direcs[self.n_edges] = self.UP
                            else:
                                self.direcs[self.n_edges] = self.DOWN
                            self.edge_sides[self.n_edges] = side
                            self.parents[self.n_edges] = parent
                            self.n_edges += 1
                    else:
                        print("Maximum number of links exceeded\n")
                        fail_ret = True
                        break
            if fail_ret:
                break
    
        if not fail_ret:
            self.n_verts -= 1
            for i in range(0, self.n_verts):
                self.verts[i][0] = self.verts[i + 1][0]

        return(not fail_ret)

    #  This method adjusts the column numbers of multiple links so that    
    #  they will not overlap each other.                                       
    def multi_links(self):
        i,j,k = 0,0,0
        while i < self.n_edges - 1:
            j = i + 1
            while j < self.n_edges and self.columns[i] == self.columns[j]:
                if self.edges[i][0] == self.edges[j][0] and self.edges[i][1] == self.edges[j][1]:
                    k = j
                    while k < self.n_edges:
                        self.columns[k] += 1
                        k += 1
                j += 1
            i += 1

    #  This method moves each link as far as possible to the left so that  
    #  the ladder will be as compact as possible. Then in updates the columns  
    #  range for each vertex (the horizontal links).                           
    def adjust_columns(self):
        for i in range(0, self.n_edges):
            if self.columns[i] > 0:
                i_min = self.n_vert(self.edges[i][0])
                i_max = self.n_vert(self.edges[i][1])
                col_min = 0
                for j in range(0, i):
                    if self.columns[j] < self.columns[i]:
                        j_min = self.n_vert(self.edges[j][0])
                        j_max = self.n_vert(self.edges[j][1])
                        if not (j_max <= i_min or i_max <= j_min):
                            col_min = max([col_min, self.columns[j] + 1])
                self.columns[i] = col_min

        for i in range(0, self.n_verts):
            self.verts[i][1] = False

        for i in range(0, self.n_edges):
            i_min = self.n_vert(self.edges[i][0])
            i_max = self.n_vert(self.edges[i][1])
            for j in range(i_min, i_max+1, i_max - i_min):
                if False == self.verts[j][1]:
                    self.verts[j][1] = True
                    self.verts[j][2] = self.columns[i]                    
                    self.verts[j][3] = self.columns[i]
                else:
                    self.verts[j][2] = min([self.verts[j][2], self.columns[i]])                    
                    self.verts[j][3] = max([self.verts[j][3], self.columns[i]])                    


    #  This method adjusts the column numbers to start from 0, and swaps   
    #  the order of vertices in the links so that the first vertex is the      
    #  lower of the two.                                                       
    def adjust_links(self):
        col_min = 0
        for i in range(0, self.n_edges):
            col_min = min([col_min, self.columns[i]])
        for i in range(0, self.n_edges):
            self.columns[i] -= col_min
            if self.n_vert(self.edges[i][0]) > self.n_vert(self.edges[i][1]):
                self.edges[i][0], self.edges[i][1] = self.edges[i][1], self.edges[i][0]
        return
        

    #  This method sorts the links by column number, and within a column   
    #  by the first vertex.                                                    
    def sort_links(self):
        i,j,k = 0,0,0

        for i in range(self.n_edges - 1, 0, -1):
            for j in range(0, i):
                if self.columns[j] > self.columns[j + 1] or (self.columns[j] == self.columns[j + 1] and self.n_vert(self.edges[j][0]) > self.n_vert(self.edges[j + 1][0])):
                    for k in range(0,2):
                        self.edges[j][k], self.edges[j+1][k] = self.edges[j+1][k], self.edges[j][k]
                    self.columns[j], self.columns[j + 1] = self.columns[j+1], self.columns[j]

