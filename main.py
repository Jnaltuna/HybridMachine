from ApnLa import ApnLa
from ClusterManager import ClusterManager
from Cluster import Cluster
from LearningAutomata import LearningAutomata


loadModified = False

apn = ApnLa(loadModified)

for i in range(2000):
    apn.fireNext()
#    if(i == 2000):
#        apn.switcharoo()

#print('Marking', apn.rdp.marking)
# for cluster in apn.clusterManager.clusters:
#    if(cluster.LA != None):
#        print('Final prob', cluster.LA.probabilityVector)
