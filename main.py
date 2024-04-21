import pandas as pd
import additionalMethods as am
import algorithms as ag
import tabuSearch as ts

if __name__ == '__main__':
    busConnections = pd.read_csv("connection_graph.csv")
    graph = am.pandasToGraph(busConnections)
    #Zad 1a)
    print("Starting calculating algorithm...")
    print(ag.dijkstraAlgorithm(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ag.astar(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ag.astarbusstop(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ag.modifiedastar(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ts.tabu_search_astar(ts.tabu_search_astar(graph, '08:29:00')))
    #Zad 2b