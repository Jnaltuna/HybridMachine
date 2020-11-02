from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np
import re


class ApnLa:

    def __init__(self, jsonFile, loadModified):

        self.rdp = Rdp(jsonFile, loadModified)

        clusterList = self.rdp.clusterlist
        print('Cluster list: ')
        for x in range(len(clusterList)):
            print(clusterList[x])
        # input()
        updateT = self.rdp.updateT
        self.clusterManager = ClusterManager(
            clusterList, updateT, jsonFile)

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)
        #print('Fired Transition:', fireTransition)
        # firedCost = self.rdp.fire(fireTransition)
        cost = self.rdp.fire(fireTransition)

        self.clusterManager.updateCost(cost, fireTransition)
        self.clusterManager.setClusterFiredTransition(fireTransition)
        self.clusterManager.setControlClusterFiredTransition(fireTransition)
        self.clusterManager.updateIfNecessary(fireTransition)

        # print(self.partialInvariants)
        #input("\nPress Enter to continue...\n")

        return

    def switcharoo(self):
        #self.rdp.costVector[0] = 50
        self.rdp.costVector[6] = 50
        self.rdp.costVector[4] = 25
        print(self.rdp.costVector)
