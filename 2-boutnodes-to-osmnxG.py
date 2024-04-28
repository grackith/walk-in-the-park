# this script takes the queried network for greenlake park, which is currently only nodes. 
# this script reads in a .csv file that contains lon_x and lat_y data from the observed walking activity. This is converted to `gdf` and added to greenlake `osmnx`.
# output is a pickle `.pkl` file: `gl-boutnodes.pkl`
import networkx as nx
import geopandas as gpd
import pandas as pd
import pickle
from shapely.geometry import Point
import osmnx as ox
ox.config(use_cache=True, log_console=True)

# Load the NetworkX graph from the pickle file
with open("/Users/gracedouglas/imitation/mal-proj/greenlake-gdf-Gnodes.pkl", "rb") as f:
    G = pickle.load(f)

# Remove all edges from the graph
G.clear_edges()

csv_file = "/Users/gracedouglas/imitation/mal-proj/april 23/nodes-for-osmnx.csv"
df = pd.read_csv(csv_file)

geometry = [Point(xy) for xy in zip(df['lon_x'], df['lat_y'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Iterate over the GeoDataFrame and add nodes with coordinates to the graph
for _, row in gdf.iterrows():
    point = (row['lon_x'], row['lat_y'])  # Extract the coordinates
    G.add_node(point)  # Add the coordinates as a node without specifying an index

# Get and print the CRS of the graph
crs = G.graph.get('crs', None)
print("CRS of the graph:", crs)

print("Connecting nodes with shortest paths...")
for u in G.nodes():
    for v in G.nodes():
        if u != v:
            shortest_path = nx.shortest_path(G, u, v)
            # Add edges along the shortest path
            for i in range(len(shortest_path) - 1):
                G.add_edge(shortest_path[i], shortest_path[i+1])
                print("edge added")

#pickle it
with open("gl-boutnodes-edges.pkl", "wb") as f:
    pickle.dump(G, f)