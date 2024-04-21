import math
import algorithms as al

def tabu_search_astar(graph, departureTime, listOfPointsToVisit,max_iterations):
    bestSolution = [([listOfPointsToVisit[0]], 0)]
    tabuList = []
    iteration = 0
    MAX_TABU_TENURE = int(math.log(len(listOfPointsToVisit)*64))

    while iteration < max_iterations:
        currentSolution = ([], 0, departureTime)
        for i in range(len(listOfPointsToVisit)-2):
            sol = al.modifiedastar(graph, listOfPointsToVisit[i], listOfPointsToVisit[i+1], currentSolution[2])
            if not sol:
                break
            currentSolution = (currentSolution[0] + sol[0][1:], currentSolution[1] + sol[1], sol[0][-1][1])
        if not currentSolution:
            break
        if currentSolution[1] < bestSolution[1]:
            bestSolution = currentSolution
        for i in range((len(currentSolution[0])-2)//2):
            tabuList.append((currentSolution[0][i], currentSolution[0][i+1]))
        if len(tabuList) > MAX_TABU_TENURE:
            tabuList.pop(0)

        iteration += 1

    return bestSolution

