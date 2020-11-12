from LearningAutomata import LearningAutomata
import numpy as np
import statistics


class Cluster:

    def __init__(self, automata, transitionList, updateT):
        self.updateT = updateT
        self.transitionList = transitionList
        self.LA = automata

        self.cost = 0
        self.historic = []
        self.transitionHistoric = []
        self.transitionMean = []
        self.meanCost = 0
        for t in transitionList:
            self.transitionHistoric.append([])
            self.transitionMean.append(0)

    def updateLA(self):

        if(self.getLastTransition() > -1):
            self.historic.append(self.cost)
            self.meanCost = self.meanCost + \
                (self.cost - self.meanCost) / len(self.historic)

        if(self.cost <= min(self.transitionMean)):
            beta = 0
        else:
            beta = 1

        self.LA.update(beta)

        self.cost = 0

        return

    def executeLA(self, enabledActions):
        fireT = self.LA.execute(enabledActions)
        return fireT

    def getLastTransition(self):
        if (self.LA != None):
            return self.LA.firedAction
        else:
            return None

    def setLastTransition(self, transition):
        if(self.LA != None):
            self.LA.firedAction = transition
    
    def updateTransitionCost(self, cost, transition):
        self.cost = cost
        tIndex = self.transitionList.index(transition)

        self.transitionHistoric[tIndex].append(cost)

        self.transitionMean[tIndex] = statistics.mean(self.transitionHistoric[tIndex][-5:])

