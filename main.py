from ApnLa import ApnLa
from ClusterManager import ClusterManager
from Cluster import Cluster
from LearningAutomata import LearningAutomata
from exceptions import NetException
import pflowEditor as editor
import argparse
import numpy as np

# TODO: definir parametros y opciones de ejecucion


def main():

    # Program arguments
    parser = argparse.ArgumentParser(description='learning automata')
    parser.add_argument('jsonFile', type=str, nargs=1)
    parser.add_argument('-n', '--num', dest='fireNumber',
                        default=100, help='number of transistions to fire')
    parser.add_argument('-r', '--rep', dest='repeat',
                        default=1, help='repeat complete execution')
    parser.add_argument('-l', '--load_mod', action='store_true',
                        help='load net wih control places')
    parser.add_argument('-m', '--mod', dest='net_name', default='null',
                        help='net to modify')
    # parser.add_argument('-o', dest='output', default='a.coe',
    #                    help='output destination')

    args = parser.parse_args()

    loadModified = args.load_mod

    f = open("results.txt", "w")
    for j in range(int(args.repeat)):
        apn = ApnLa(args.jsonFile[0], loadModified)

        for i in range(int(args.fireNumber)):
            try:
                apn.fireNext()
            except NetException:
                print("Red bloqueada - se anula la ejecucion")
                break
            # if(i == 1000):
            #    apn.switcharoo()
        for cluster in apn.clusterManager.clusters:
            if(cluster.LA != None):
                f.write(np.array2string(cluster.LA.probabilityVector))
        f.write('\n')

    if args.net_name != 'null':
        petriShape = editor.obtain_elements(
            apn.rdp.iPlusMatrix, apn.rdp.iMinusMatrix, apn.rdp.inhibitionMatrix, apn.rdp.initialMarking)

        newTransitions = petriShape.transitions[-(len(apn.rdp.updateT)-1):]
        newPlaces = petriShape.places[-len(newTransitions)*2:]
        newArcs = []

        for arc in petriShape.arcs:
            for place in newPlaces:
                if arc.srcId == place.label or arc.dstId == place.label:
                    newArcs.append(arc)

        editor.modify_net(args.net_name, newPlaces, newTransitions, newArcs)

    # print('Marking', apn.rdp.marking)
    # for cluster in apn.clusterManager.clusters:
    #    if(cluster.LA != None):
    #        print('Final prob', cluster.LA.probabilityVector)


if __name__ == "__main__":
    main()
