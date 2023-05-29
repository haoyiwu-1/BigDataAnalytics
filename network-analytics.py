# Importing needed libraries
import argparse
import pandas as pd
import networkx as nx

# Creating the parser to be used
parser = argparse.ArgumentParser()

# Adding arguments to match the needed command line arguments
# Argument for the file or filename or filepath
parser.add_argument('filepath', type = str)

# Parsing the argument
args = parser.parse_args()

# Setting variables arguments
filepath = args.filepath  # variable for filepath

# Variable to hold edge count
edges = 0

# Opening edge file
edge_list = open(filepath, 'r')
# Reading all edges from edge file
lines = edge_list.readlines()

# Initializing vertex set
vertex_set = set()

# List to hold all nodes / vertices
all_nodes = []

# Map to map node degree of each node
node_degrees = {}

# Loop through the edges in the edge file 
for line in lines:
    # increment the edge count by 1 for each edge in file
    edges += 1
    # Split the edge into 2 vertices
    vertices = line.split(' ')
    # Loop through the vertices and add to vertex set and all nodes list
    for vertex in vertices:
        vertex_set.add(vertex.strip())
        all_nodes.append(vertex.strip())

# Loop through all the vertices in all_nodes list to find degrees
for vertex in all_nodes:
    # Either add new node to node_degree dictionary
    # Or increment an existing value
    if vertex in node_degrees:
        node_degrees[vertex] += 1
    else:
        node_degrees[vertex] = 1

# Set total degree of graph / network to 0 
total_degree = 0

# Loop through all values in node_degrees to get total degree of graph
for degree in node_degrees.values():
    total_degree += degree

# Create graph using networkx package
G = nx.read_edgelist(filepath, create_using = nx.Graph(), nodetype = str)

# Write wanted results to file
with open('Q4.out', 'w') as f:
    # Write vertex count from vertex_set and number of edges
    f.write(str(len(vertex_set)) + " " + str(edges) + "\n")
    # Calculate average degree of nodes and write to file
    # Given this is an average use round()
    f.write(str(round(total_degree / len(vertex_set), 2)) + "\n")
    # Get number of connected components using networkx package
    # Write result to file
    f.write(str(nx.number_connected_components(G)) + "\n")
    # Get number of triangles using networkx package
    # Write result to file
    f.write(str(int(len(nx.triangles(G)) / 3)) + "\n")
# Closing file after writing
f.close()