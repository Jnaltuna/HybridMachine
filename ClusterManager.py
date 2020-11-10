from Cluster import Cluster
from LearningAutomata import LearningAutomata
import numpy as np
import random
import json
import statistics


class ClusterManager:

    def __init__(self, clusterList, updateT, control, tInvariants):
        self.updateT = updateT
        self.clusters = []
        self.controlClusters = []

        for i in range(len(clusterList)):
            automata = None
            if (i != 0):
                automata = LearningAutomata(clusterList[i])
            cluster = Cluster(automata, clusterList[i], updateT[i])

            if (control[i] == False):
                self.clusters.append(cluster)
            else:
                self.controlClusters.append(cluster)

        self.invCost = []
        for inv in tInvariants:
            self.invCost.append(0)
        self.tInvariants = tInvariants
        #self.cost = 0
        self.historic = []
        self.meanCost = 0

    def updateCost(self, cost, invNum):

        self.invCost[invNum] = cost
        self.historic.append(cost)
        self.meanCost = self.meanCost + \
            (cost - self.meanCost) / len(self.historic)
        #self.meanCost = statistics.mean(self.historic[-50:])
        #print('Cost: ', cost)
        #print('Mean: ', self.meanCost)

        return

    def updateIfNecessary(self, numT):
        if self.isUpdate(numT):
            cluster = self.getClusterFromUpdate(self.clusters, numT)
            if cluster == None:
                cluster = self.getClusterFromUpdate(self.controlClusters, numT)

            cost = []
            for tinv in self.tInvariants:
                if (cluster.LA.firedAction in tinv):
                    cost.append(self.invCost[self.tInvariants.index(tinv)])

            cost = [val for val in cost if val != 0]

            if not cost:
                return

            cluster.updateLA(min(cost), self.meanCost)

    def getClusterFromUpdate(self, clusterList, numT):
        for cluster in clusterList:
            if(numT == cluster.updateT):
                return cluster
        return None

    def isUpdate(self, transition):
        if transition in self.updateT:
            return True
        else:
            return False

    def localEnabledList(self, transitionList, enabledList):
        localEnList = []

        for i in range(len(enabledList)):
            if (enabledList[i] == True) and (i in transitionList):
                localEnList.append(i)
        return localEnList

    # returns transition to fire based on enabled vector
    def getFireTransition(self, enabledTransitions):

        selectedCluster, localEnabled = self.getFireCluster(enabledTransitions)

        selectedTransition = -1
        if(selectedCluster == None):
            selectedTransition = localEnabled[0]
        else:
            if self.clusters.index(selectedCluster) == 0:
                selectedTransition = random.choice(localEnabled)
            else:
                selectedTransition = selectedCluster.executeLA(localEnabled)

        return selectedTransition

    def getFireCluster(self, enabled):

        enabledClusters = self.enabledClusters(enabled)

        if(len(enabledClusters[0]) > 0):
            controlCluster, clusterEnabledTransitions = self.selectCluster(
                enabled, enabledClusters[0])
            selectedTransition = controlCluster.executeLA(
                clusterEnabledTransitions)
            for cluster in enabledClusters[1]:
                if (selectedTransition in cluster.transitionList):
                    return cluster, self.getClusterEnabledTransitions(cluster, enabled)
            return None, [selectedTransition]
        else:
            return self.selectCluster(enabled, enabledClusters[1])

        #TODO: CAMBIAR
        # for cluster in enabledClusters:
        #     localEnabled = self.getClusterEnabledTransitions(
        #         cluster, enabled)
        #     clusterProb.append(len(localEnabled)/len(enabled))
        #     clusterEnabledTransitions.append(localEnabled)
        # selectedCluster = random.choices(enabledClusters, clusterProb, k=1)[-1]

        # return selectedCluster, clusterEnabledTransitions[enabledClusters.index(selectedCluster)]

    def enabledClusters(self, enabledTransitions):

        enabledClusters = []

        enabledClusters.append([])

        for cluster in self.controlClusters:
            for t in range(len(enabledTransitions)):
                if(enabledTransitions[t]):
                    if(t in cluster.transitionList):
                        enabledClusters[0].append(cluster)
                        break

        enabledClusters.append([])

        for cluster in self.clusters:
            for t in range(len(enabledTransitions)):
                if(enabledTransitions[t]):
                    if(t in cluster.transitionList):
                        enabledClusters[1].append(cluster)
                        break

        return enabledClusters

    def getClusterEnabledTransitions(self, cluster, enabledTransitions):

        localEnabled = []

        for t in cluster.transitionList:
            if enabledTransitions[t] == True:
                localEnabled.append(t)

        return localEnabled

    def selectCluster(self, enabledTransitions, enabledClusters):
        clusterProb = []
        clusterEnabledTransitions = []

        for cluster in enabledClusters:
            localEnabled = self.getClusterEnabledTransitions(
                cluster, enabledTransitions)
            clusterProb.append(len(localEnabled)/len(enabledTransitions))
            clusterEnabledTransitions.append(localEnabled)
        selectedCluster = random.choices(enabledClusters, clusterProb, k=1)[-1]

        return selectedCluster, clusterEnabledTransitions[enabledClusters.index(selectedCluster)]

    def resolveConflict(self, cluster, enabledList):
        actions = self.localEnabledList(
            self.clusters[cluster].transitionList, enabledList)
        return self.clusters[cluster].executeLA(actions)

    def setClusterFiredTransition(self, transition):
        for cluster in self.clusters:
            if(transition in cluster.transitionList):
                cluster.setLastTransition(transition)