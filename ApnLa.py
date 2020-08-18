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

        # TODO test
        test = [False, True, False, False, False, False,
                False, False, False, False, False, False]

        print(self.clusterManager.resolveConflict(1, test))

    def fireNext(self):

        enabled = self.rdp.calcularSensibilizadas()

        selectedCluster = self.clusterManager.selectCluster(enabled)

        if selectedCluster == 0:
            print('')
        else:
            print('')
