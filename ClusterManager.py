from Cluster import Cluster
from LearningAutomata import LearningAutomata
import numpy as np
import random


class ClusterManager:

    def __init__(self, clusterList, updateT):
        self.updateT = updateT
        self.clusters = []
        for i in range(len(clusterList)):
            automata = None
            if (i != 0):
                automata = LearningAutomata(clusterList[i])
            self.clusters.append(Cluster(automata, clusterList[i], updateT[i]))

    def updateIfNecessary(self, numT):
        if numT in self.updateT:
            clusterIndex = self.updateT.index(numT)
            self.clusters[clusterIndex].updateLA()

    def resolveConflict(self, cluster, enabledList):
        actions = self.localEnabledList(
            self.clusters[cluster].transitionList, enabledList)
        return self.clusters[cluster].executeLA(actions)

    def updateCost(self, cost):
        # TODO update cost of every cluster
        return

    def localEnabledList(self, transitionList, enabledList):
        localEnList = []

        for i in range(len(enabledList)):
            if (enabledList[i] == True) and (i in transitionList):
                localEnList.append(i)
        return localEnList

    def selectCluster(self, enabled):

        clusterProb = []

        enabledClusters = self.enabledClusters(enabled)

        for cluster in enabledClusters:
            enabledTransitions = self.clusterEnabledTransitions(
                cluster, enabledTransitions)
            clusterProb.append(len(enabledTransitions)/len(enabled))

        selectedCluster = random.choices(enabledClusters, clusterProb, k=1)
        print(selectedCluster)

        return selectedCluster

    def enabledClusters(self, enabledTransitions):

        enabledClusters = []

        for cluster in self.clusters:
            for t in range(enabledTransitions):
                if(enabledTransitions[t]):
                    if(t in cluster.transitionList):
                        enabledClusters.append(cluster)
                        break

        return enabledClusters

    def clusterEnabledTransitions(self, cluster, enabledTransitions):

        enabledTransitions = []

        for t in cluster.transitionList:
            if enabledTransitions[t] == True:
                enabledTransitions.append(True)

        return enabledTransitions
