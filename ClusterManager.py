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

    def updateCost(self, cost, transition):
        # TODO update cost of every cluster
        for cluster in self.clusters:
            cluster.cost += cost

        self.updateIfNecessary(transition)
        return

    def localEnabledList(self, transitionList, enabledList):
        localEnList = []

        for i in range(len(enabledList)):
            if (enabledList[i] == True) and (i in transitionList):
                localEnList.append(i)
        return localEnList

    def selectCluster(self, enabled):

        clusterProb = []
        clusterEnabledTransitions = []

        enabledClusters = self.enabledClusters(enabled)

        for cluster in enabledClusters:
            localEnabled = self.getClusterEnabledTransitions(
                cluster, enabled)
            clusterProb.append(len(localEnabled)/len(enabled))
            clusterEnabledTransitions.append(localEnabled)

        selectedCluster = random.choices(enabledClusters, clusterProb, k=1)[-1]

        return selectedCluster, clusterEnabledTransitions[enabledClusters.index(selectedCluster)]

    def enabledClusters(self, enabledTransitions):

        enabledClusters = []

        for cluster in self.clusters:
            for t in range(len(enabledTransitions)):
                if(enabledTransitions[t]):
                    if(t in cluster.transitionList):
                        enabledClusters.append(cluster)
                        break

        return enabledClusters

    def getClusterEnabledTransitions(self, cluster, enabledTransitions):

        localEnabled = []

        for t in cluster.transitionList:
            if enabledTransitions[t] == True:
                localEnabled.append(t)

        return localEnabled

    def getFireTransition(self, enabledTransitions):

        selectedCluster, localEnabled = self.selectCluster(enabledTransitions)
        selectedTransition = -1

        if self.clusters.index(selectedCluster) == 0:
            selectedTransition = random.choice(localEnabled)
        else:
            selectedTransition = selectedCluster.executeLA(localEnabled)

        return selectedTransition
