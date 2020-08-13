from Rdp import Rdp
from ClusterManager import ClusterManager


class ApnLa:

    def __init__(self, loadModified):
        if loadModified:
            self.rdp = Rdp(True)
            clusterList = self.rdp.clusterlist
            updateT = self.rdp.updateT
        else:
            self.rdp = Rdp(False)
            clusterList = self.rdp.defineClusterList()
            print('Implementar luego')

        self.clusterManager = ClusterManager(clusterList, updateT)
