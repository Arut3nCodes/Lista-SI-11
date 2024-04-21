import pandas as pd
import additionalMethods as am
import algorithms as ag
import tabuSearch as ts

def uniqueInOrder(seq):
    uniqueElements = []
    for item in seq:
        if not uniqueElements or item != uniqueElements[-1]:
            uniqueElements.append(item)
    return uniqueElements

if __name__ == '__main__':
    busConnections = pd.read_csv("connection_graph.csv")
    graph = am.pandasToGraph(busConnections)

    while True:
        startNode = input("Enter startNode: ")
        if startNode not in graph.nodes():
            print("Invalid startNode. Please enter a valid start stop.")
            continue

        endNode = input("Enter endNode: ")
        if endNode not in graph.nodes():
            print("Invalid endNode. Please enter a valid end stop.")
            continue

        timeStr = input("Enter time (hh:mm): ")
        timeParts = timeStr.split(":")
        if len(timeParts) != 2:
            print("Invalid time format. Please provide hh:mm.")
            continue

        try:
            hours = int(timeParts[0])
            minutes = int(timeParts[1])
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError
        except ValueError:
            print("Invalid time format. Hours must be between 00 and 23, and minutes between 00 and 59.")
            continue

        print("Valid input. startNode:", startNode, "endNode:", endNode, "time:", timeStr + ":00")
        break

    #Zad 1a)
    print("Starting calculating algorithm...")
    ((path, arrivalTime, linesUsed), cost) = ag.dijkstraAlgorithm(graph, startNode, endNode, timeStr + ":00")
    print("Sciezka: " + str(path))
    print("Zakonczenie podrozy: " + arrivalTime)
    print("Uzyte linie" + str(uniqueInOrder(linesUsed)))
    print("Koszt " + str(cost))
   # print(ag.astar(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ag.astarbusstop(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ag.modifiedastar(graph, 'Rogowska (P+R)', 'most Grunwaldzki', '08:29:00'))
   # print(ts.tabu_search_astar(ts.tabu_search_astar(graph, '08:29:00')))
   # Zad 2b

