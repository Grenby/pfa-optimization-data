import networkx as nx
import osmnx as ox
import pandas


def get_graph(city_id: str) -> nx.Graph:
    gdf = ox.geocode_to_gdf(city_id, by_osmid=True)
    polygon_boundary = gdf.unary_union
    graph = ox.graph_from_polygon(polygon_boundary,
                                  network_type='drive',
                                  simplify=True)
    G = nx.Graph(graph)
    H = nx.Graph()
    # add edges in H, copy only weight
    for u, d in G.nodes(data=True):
        H.add_node(u, x=d['x'], y=d['y'])
    for u, v, d in G.edges(data=True):
        H.add_edge(u, v, length=d['length'])
    del city_id, gdf, polygon_boundary, graph, G
    return H


if __name__ == '__main__':
    file_name = 'osm_city_ids.csv'
    df = pandas.read_csv(file_name)
    G = get_graph(df.iloc[0]['id'])
    print(len(G.nodes))