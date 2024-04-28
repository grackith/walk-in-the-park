# this script queries open street maps `osm` for green lake park, where we have naturalistic observations of pedestrian walking activity. 
# output is a pickle `.pkl` file: `greenlake-gdf-Gnodes.pkl`

import pickle
import osmnx as ox

ox.config(use_cache=True, log_console=True)

address = "Green Lake Park, Seattle, WA"
gdf = ox.geocode_to_gdf(address)
G = ox.graph_from_address(address, retain_all=True, network_type='all', dist=5000)

# graph with only nodes
gdf_nodes = ox.graph_to_gdfs(G, nodes=True, edges=False)

with open("greenlake-gdf-Gnodes.pkl", "wb") as f:
    pickle.dump(G, f)