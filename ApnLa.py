from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np


class ApnLa:

    def __init__(self, jsonFile, loadModified):

        self.rdp = Rdp(jsonFile, loadModified)

        clusterList = self.rdp.clusterlist
        print('Cluster list: ')
        for x in range(len(clusterList)):
            print(clusterList[x])
        updateT = self.rdp.updateT
        self.clusterManager = ClusterManager(clusterList, updateT)

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)
        print('Fired Transition:', fireTransition)
        firedCost = self.rdp.fire(fireTransition)

        self.clusterManager.updateCost(firedCost, fireTransition)

        return

    def switcharoo(self):
        self.rdp.costVector[0] = 10
