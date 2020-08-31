from ApnLa import ApnLa
from ClusterManager import ClusterManager
from Cluster import Cluster
from LearningAutomata import LearningAutomata
import pflowEditor as editor

# TODO: definir parametros y opciones de ejecucion

loadModified = False

apn = ApnLa(loadModified)

# for i in range(2000):
#    apn.fireNext()

#nr.modify_net('P15', '10', ['T1', 'T2'], ['T3', 'T4'])
# nr.addTransition(90)
#nr.addArc('regular', 'P1', 'T8', '8')
petriShape = editor.obtain_elements(
    apn.rdp.iPlusMatrix, apn.rdp.iMinusMatrix, apn.rdp.inhibitionMatrix, apn.rdp.initialMarking)

newTransitions = petriShape.transitions[-(len(apn.rdp.updateT)-1):]
newPlaces = petriShape.places[-len(newTransitions)*2:]
newArcs = []

for arc in petriShape.arcs:
    for place in newPlaces:
        if arc.srcId == place.label or arc.dstId == place.label:
            newArcs.append(arc)

editor.modify_net(newPlaces, newTransitions, newArcs)
#    if(i == 2000):
#        apn.switcharoo()

#print('Marking', apn.rdp.marking)
# for cluster in apn.clusterManager.clusters:
#    if(cluster.LA != None):
#        print('Final prob', cluster.LA.probabilityVector)
