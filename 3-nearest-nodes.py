# this script accepts nodes in a gdf.
# read in a combined gdf wiith both osm nodes and bout nodes. The edges have been previously removed `.drop_edges()`. Now we must reconnect.
# we should make everything bidirectional..ouch
# we should project the network (set a crs) before doing any euclidean computations edge-wise. 
# we should ensure the nodes we have are unique


import networkx as nx
import geopandas as gpd
import pandas as pd
import pickle
from shapely.geometry import Point
import matplotlib.pyplot as plt
import osmnx as ox
ox.config(use_cache=True, log_console=True)

with open("gl-boutnodes.pkl", "rb") as f:
    G = pickle.load(f)
t= type(G)
print(G)
# nodes got data?
# for node, data in G.nodes(data=True):
#     if "x" not in data or "y" not in data:
#         print(f"Node {node} is missing coordinate data.")
#     else:
#         print(f"Node {node} has coordinates ({data['x']}, {data['y']}).")

target_crs = "EPSG:32610"  # UTM zone 10N for Seattle
G_epsg32610 = ox.projection.project_graph(G, to_crs=target_crs)

# G is a graph. We must ensure we have unique nodes before we add edges between ndoes.
unique_nodes = set(G.nodes())
unique_graph = G.subgraph(unique_nodes)
print(f"Original graph (G) has {len(G.nodes())} nodes and {len(G.edges())} edges.")
print(f"Unique graph (unique_graph) has {len(unique_graph.nodes())} nodes and {len(unique_graph.edges())} edges.")

#Connect each node to its nearest neighbor, but we want to keep things `connected`, lets go shortest path
print("Connecting nodes with shortest paths...")

for source in unique_nodes:
    for target in unique_nodes:
        if source != target:
            shortest_path = nx.shortest_path(unique_graph, source, target)
            # Add edges along the shortest path
            for i in range(len(shortest_path) - 1):
                unique_graph.add_edge(shortest_path[i], shortest_path[i+1])

print("Shortest path connections completed.")