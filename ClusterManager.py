from Cluster import Cluster


class ClusterManager:

    def __init__(self, clusterList, updateT):
        self.updateT = updateT
        self.clusters = []
        for i in range(len(clusterList)):
            self.clusters.append(Cluster(clusterList[i], updateT[i]))
        for i in range(0, 13):
            self.updateIfNecessary(i)

    def updateIfNecessary(self, numT):
        if numT in self.updateT:
            clusterIndex = self.updateT.index(numT)
            self.clusters[clusterIndex].updateLA()

    def resolveConflict(self, cluster, enabledList):
        print('')

    def updateCost(self, cost):
        # TODO update cost of every cluster
        return
