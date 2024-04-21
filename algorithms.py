import heapq
import math

import networkx


def timeToMinutes(timeStr):
    hour, minute, seconds = map(int, timeStr.split(':'))
    total_minutes = hour * 60 + minute
    return total_minutes

def edgeCostByTime(graph : networkx.MultiDiGraph, startNode, endNode, currTime):
    currEdge = None
    print(startNode + ' ' + endNode + ' ' +currTime, end=" ")
    edges = graph[startNode][endNode].items()
    print(len(edges), end=" ")
    edges = filter(lambda x: timeToMinutes(x[1]['departure_time']) >= timeToMinutes(currTime), edges)
    edges = sorted(edges, key=lambda x: timeToMinutes(x[1]['departure_time']))
    print(len(edges))
    if edges:
        currEdge = (next(iter(edges)))
        if currEdge != None:
            return timeToMinutes(currEdge[1]['arrival_time']) - timeToMinutes(currTime), currEdge[1]['arrival_time'], currEdge[1]
    return None
def edgeCostByTimeAndChangingLines(graph, startNode, endNode, currTime, currLine):
    currEdge = None
    print(startNode + ' ' + endNode + ' ' + currTime, end=" ")
    edges = graph[startNode][endNode].items()
    print(len(edges), end=" ")
    edges = filter(lambda x: timeToMinutes(x[1]['departure_time']) >= timeToMinutes(currTime), edges)
    edges = sorted(edges, key=lambda x: timeToMinutes(x[1]['departure_time']))
    print(len(edges))
    if edges:
        currEdge = (next(iter(edges)))
        if currEdge != None:
            changeLinePunishment = 30 if currLine != currEdge['line'] else 0
            return (timeToMinutes(currEdge['arrival_time']) - timeToMinutes(currTime)) + changeLinePunishment, currEdge['arrival_time'], currEdge
    return None

def heurestic(graph, startNode, endNode):
    for (start, end, edge) in graph.edges(data=True):
        if start == startNode and end == endNode:
            return abs(edge['start_stop_lat'] - edge['end_stop_lat']) + abs(edge['start_stop_lon'] - edge['end_stop_lon'])

def reconstructPath(dict, endNode):
    currNode = endNode
    path = [currNode]
    while dict[currNode] != None:
        currNode = dict[currNode]
        path = path + [currNode]
    return path.reverse()

def dijkstraAlgorithm(graph, startNode, endNode, departureTime):
    #for node in graph.nodes():
        #print(node)
        #print(list(graph.neighbors(node)))
    #print(startNode)
    checkedNodes = set()
    nodeQueue = [(0, startNode)]
    costDict = {startNode: 0}
    pathDict = {startNode: ([startNode], departureTime, [])}

    for node in graph.nodes():
        if(node not in costDict.keys()):
            costDict[node] = math.inf

    while nodeQueue:
        (currNodeCost, currNode) = heapq.heappop(nodeQueue)
        print(currNode)
        (currPath, currTime, currLineList) = pathDict[currNode]
        #print(list(graph.neighbors(currNode)))
        if(currNode == endNode):
            break
        for neighbor in graph.neighbors(currNode):
            costTuple = edgeCostByTime(graph, currNode, neighbor, currTime)
            #print(neighbor, costTuple)
            if costTuple is not None:
                edgeCost, arrivalTime, data = costTuple
                currCost = currNodeCost + edgeCost
                if neighbor not in checkedNodes and neighbor is not endNode:
                    heapq.heappush(nodeQueue, (currCost, neighbor))
                    checkedNodes.add(neighbor)
                if (neighbor not in costDict.keys()):
                    costDict[neighbor] = currCost
                    pathDict[neighbor] = (currPath + [neighbor], arrivalTime, currLineList + [data['line']])
                else:
                    if (costDict[neighbor] > edgeCost):
                        costDict[neighbor] = currCost
                        pathDict[neighbor] = (currPath + [neighbor], arrivalTime, currLineList + [data['line']])
    #print(pathDict, costDict)
    return pathDict[endNode], costDict[endNode]

def astar(graph, startNode, endNode, departureTime):
    #for node in graph.nodes():
        #print(node)
        #print(list(graph.neighbors(node)))
    #print(startNode)
    checkedNodes = set()
    nodeQueue = [startNode]
    costDict = {startNode: 0}
    pathDict = {startNode: ([startNode], departureTime)}

    for node in graph.nodes():
        if(node not in costDict.keys()):
            costDict[node] = math.inf

    while nodeQueue:
        currNode = nodeQueue.pop(0)
        #print(currNode)
        (currPath, currTime) = pathDict[currNode]
        #print(list(graph.neighbors(currNode)))
        for neighbor in graph.neighbors(currNode):
            #print(neighbor)
            costTuple = edgeCostByTime(graph, currNode, neighbor, currTime)
            #print(neighbor, costTuple)
            if costTuple is not None:
                if (neighbor not in checkedNodes):
                    nodeQueue.append(neighbor)
                    checkedNodes.add(neighbor)
                if (neighbor not in costDict.keys()):
                    edgeCost, arrivalTime, data = costTuple
                    costDict[neighbor] = costDict[currNode] + edgeCost + heurestic(graph, startNode, endNode) * 500
                    pathDict[neighbor] = (currPath + [neighbor], arrivalTime)
                    currLine = data['line']
                else:
                    newCost, arrivalTime, data = costTuple
                    if (costDict[neighbor] > newCost):
                        costDict[neighbor] = costDict[currNode] + newCost + heurestic(graph, startNode, endNode) * 500
                        pathDict[neighbor] = (currPath + [neighbor], arrivalTime)
                        currLine = data['line']
    #print(pathDict, costDict)
    return pathDict[endNode], costDict[endNode]

def astarbusstop(graph, startNode, endNode, departureTime):
    #for node in graph.nodes():
        #print(node)
        #print(list(graph.neighbors(node)))
    #print(startNode)
    checkedNodes = set()
    nodeQueue = [startNode]
    costDict = {startNode: 0}
    pathDict = {startNode: ([startNode], departureTime)}
    currLine = None

    for node in graph.nodes():
        if(node not in costDict.keys()):
            costDict[node] = math.inf

    while nodeQueue:
        currNode = nodeQueue.pop(0)
        #print(currNode)
        (currPath, currTime) = pathDict[currNode]
        #print(list(graph.neighbors(currNode)))
        for neighbor in graph.neighbors(currNode):
            #print(neighbor)
            costTuple = edgeCostByTimeAndChangingLines(graph, currNode, neighbor, currTime, currLine)
            #print(neighbor, costTuple)
            if costTuple is not None:
                if (neighbor not in checkedNodes):
                    nodeQueue.append(neighbor)
                    checkedNodes.add(neighbor)
                if (neighbor not in costDict.keys()):
                    edgeCost, arrivalTime, _ = costTuple
                    costDict[neighbor] = costDict[currNode] + edgeCost + heurestic(graph, startNode, endNode) * 500
                    pathDict[neighbor] = (currPath + [neighbor], arrivalTime)
                else:
                    newCost, arrivalTime, _ = costTuple
                    if (costDict[neighbor] > newCost):
                        costDict[neighbor] = costDict[currNode] + newCost + heurestic(graph, startNode, endNode) * 500
                        pathDict[neighbor] = (currPath + [neighbor], arrivalTime)
    #print(pathDict, costDict)
    return pathDict[endNode], costDict[endNode]

def modifiedastar(graph, startNode, endNode, departureTime):
    #for node in graph.nodes():
        #print(node)
        #(list(graph.neighbors(node)))
    #print(startNode)
    checkedNodes = set()
    nodeQueue = [startNode]
    costDict = {startNode: 0}
    pathDict = {startNode: (None, departureTime)}

    for node in graph.nodes():
        if(node not in costDict.keys()):
            costDict[node] = math.inf

    while nodeQueue:
        currNode = nodeQueue.pop(0)
        (currPath, currTime) = pathDict[currNode]
        for neighbor in graph.neighbors(currNode):
            if(currNode == endNode):
                continue
            print(neighbor)
            costTuple = edgeCostByTime(graph, currNode, neighbor, currTime)
            print(neighbor, costTuple)
            if costTuple is not None and (costDict[endNode] is None or costDict[endNode] > costTuple[0]):
                if (neighbor not in checkedNodes):
                    nodeQueue.append(neighbor)
                    checkedNodes.add(neighbor)
                if (neighbor not in costDict.keys()):
                    edgeCost, arrivalTime, data = costTuple
                    costDict[neighbor] = costDict[currNode] + edgeCost + heurestic(graph, startNode, endNode)  * 500
                    pathDict[neighbor] = (currNode, arrivalTime, data['line'])
                    currLine = data['line']
                else:
                    newCost, arrivalTime, data = costTuple
                    if (costDict[neighbor] > newCost):
                        costDict[neighbor] = costDict[currNode] + newCost + heurestic(graph, startNode, endNode)  * 500
                        pathDict[neighbor] = (currNode, arrivalTime, data['line'])
                        currLine = data['line']
    #print(pathDict, costDict)
    return pathDict[endNode], costDict[endNode]

def modifiedastartabu(graph, startNode, endNode, departureTime, tabu):
    #for node in graph.nodes():
        #print(node)
        #(list(graph.neighbors(node)))
    #print(startNode)
    checkedNodes = set()
    nodeQueue = [startNode]
    costDict = {startNode: 0}
    pathDict = {startNode: (None, departureTime)}

    for node in graph.nodes():
        if(node not in costDict.keys()):
            costDict[node] = math.inf

    while nodeQueue:
        currNode = nodeQueue.pop(0)
        (currPath, currTime) = pathDict[currNode]
        for neighbor in graph.neighbors(currNode):
            if(currNode == endNode or (currNode, neighbor) in tabu):
                continue
            print(neighbor)
            costTuple = edgeCostByTime(graph, currNode, neighbor, currTime)
            print(neighbor, costTuple)
            if costTuple is not None and (costDict[endNode] is None or costDict[endNode] > costTuple[0]):
                if (neighbor not in checkedNodes):
                    nodeQueue.append(neighbor)
                    checkedNodes.add(neighbor)
                if (neighbor not in costDict.keys()):
                    edgeCost, arrivalTime, data = costTuple
                    costDict[neighbor] = costDict[currNode] + edgeCost + heurestic(graph, startNode, endNode)  * 500
                    pathDict[neighbor] = (currNode, arrivalTime, data['line'])
                    currLine = data['line']
                else:
                    newCost, arrivalTime, data = costTuple
                    if (costDict[neighbor] > newCost):
                        costDict[neighbor] = costDict[currNode] + newCost + heurestic(graph, startNode, endNode)  * 500
                        pathDict[neighbor] = (currNode, arrivalTime, data['line'])
                        currLine = data['line']
    #print(pathDict, costDict)
    return pathDict[endNode], costDict[endNode]
