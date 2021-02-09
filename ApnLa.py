from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np
import re


class ApnLa:

    def __init__(self, jsonFile, loadModified):

        self.rdp = Rdp(jsonFile, loadModified)

        clusterList = self.rdp.clusterlist
        updateT = self.rdp.updateT
        self.clusterManager = ClusterManager(
            clusterList, updateT, self.rdp.controlConflicts)

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)

        cost = self.rdp.fire(fireTransition)

        self.clusterManager.updateCost(cost, fireTransition)
        self.clusterManager.setClusterFiredTransition(fireTransition)
        self.clusterManager.setControlClusterFiredTransition(fireTransition)
        self.clusterManager.updateIfNecessary(fireTransition)

        return

    def switcharoo(self):
        self.rdp.costVector[6] = 50
        self.rdp.costVector[4] = 25
        print(self.rdp.costVector)

    def printClusters(self):
        print("\nCLUSTERS:\n")
        print("\tRegular clusters")
        for cluster in self.clusterManager.clusters:
            print('\t\t*',cluster.transitionList)
        if (len(self.clusterManager.controlClusters) > 0):
            print("\tControl clusters")
            for cluster in self.clusterManager.controlClusters:
                print('\t\t*',cluster.transitionList)

    def getClusterProbs(self):
        probs=[]
        for cluster in self.clusterManager.clusters:
            if (cluster.LA != None):
                probs.append(cluster.LA.probabilityVector.tolist())
        for cluster in self.clusterManager.controlClusters:
            probs.append(cluster.LA.probabilityVector.tolist())
        return probs

    def getClusterTransitions(self):
        labels = []
        for cluster in self.clusterManager.clusters:
            if (cluster.LA != None):
                labels.append(cluster.transitionList)
        for cluster in self.clusterManager.controlClusters:
            labels.append(cluster.transitionList)
        return labels
