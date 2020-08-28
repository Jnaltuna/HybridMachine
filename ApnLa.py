from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np


class ApnLa:

    def __init__(self, loadModified):
        if loadModified:
            self.rdp = Rdp(True)
        else:
            self.rdp = Rdp(False)

        clusterList = self.rdp.clusterlist
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
