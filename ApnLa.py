from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np


class ApnLa:

    def __init__(self, loadModified):
        if loadModified:
            self.rdp = Rdp(True)
            clusterList = self.rdp.clusterlist
            updateT = self.rdp.getUpdateT()
        else:
            self.rdp = Rdp(False)
            clusterList = self.rdp.defineClusterList()
            print('Implementar luego')

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
