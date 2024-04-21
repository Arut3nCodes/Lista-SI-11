import csv
import networkx as nx

# def pandasToGraph(df):
#     G = nx.MultiGraph()
#     for _, row in df.iterrows():
#         G.add_node(row['start_stop'])
#         G.add_node(row['end_stop'])
#
#         # Dodawanie krawędzi do grafu
#         G.add_edge(row['start_stop'], row['end_stop'],
#                    line=row['line'],
#                    departure_time=row['departure_time'],
#                    arrival_time=row['arrival_time'],
#                    start_lat=row['start_stop_lat'],
#                    start_lon=row['start_stop_lon'],
#                    end_lat=row['end_stop_lat'],
#                    end_lon=row['end_stop_lon'])
#     return G

import networkx as nx
import concurrent.futures


# def pandasToGraph(df):
#     print('started processing')
#     G = nx.MultiDiGraph()
#     for _, row in df.iterrows():
#         G.add_node(row['start_stop'])
#         G.add_node(row['end_stop'])
#
#         # Dodawanie krawędzi do grafu
#         G.add_edge(row['start_stop'], row['end_stop'],
#                    line=row['line'],
#                    departure_time=row['departure_time'],
#                    arrival_time=row['arrival_time'],
#                    start_lat=row['start_stop_lat'],
#                    start_lon=row['start_stop_lon'],
#                    end_lat=row['end_stop_lat'],
#                    end_lon=row['end_stop_lon'])
#     print('finished processing')
#     return G

import networkx as nx

def pandasToGraph(df):
    print('started processing')
    G = nx.MultiDiGraph()

    # Create a set to store already added nodes
    added_nodes = set()

    # Add nodes from both start and end stops
    added_nodes.update(df['start_stop'].unique())
    added_nodes.update(df['end_stop'].unique())
    G.add_nodes_from(added_nodes)

    # Add edges to the graph
    edges = df.apply(lambda row: (row['start_stop'], row['end_stop'], {
        'line': row['line'],
        'departure_time': row['departure_time'],
        'arrival_time': row['arrival_time'],
        'start_lat': row['start_stop_lat'],
        'start_lon': row['start_stop_lon'],
        'end_lat': row['end_stop_lat'],
        'end_lon': row['end_stop_lon']
    }), axis=1)
    G.add_edges_from(edges)

    print('finished processing')
    return G
