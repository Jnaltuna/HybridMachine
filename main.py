from ApnLa import ApnLa
from ClusterManager import ClusterManager
from Cluster import Cluster
from LearningAutomata import LearningAutomata
from exceptions import NetException
import pflowEditor as editor
import argparse
import numpy as np


def main():

    args = getArgs()

    loadModified = args.load_mod
    verbose = args.verbose
    pflowFile = args.net_name
    transitionsToFire = args.fireNumber
    totalIterations = args.repeat

    f = open("results.txt", "w")
    for j in range(int(totalIterations)):
        block = False
        print("Inicializando iteracion ",j)
        apn = ApnLa(args.jsonFile[0], loadModified)

        if(verbose):
            apn.printClusters()

        for i in range(1, int(transitionsToFire)+1):
            try:
                apn.fireNext()
            except NetException:
                print("Red bloqueada - se anula la ejecucion")
                block = True
                break

            if (verbose and i % 2000 == 0):
                print(i)
                printClustersProbabilities(apn)

        if block != True:
            writeResults(f, apn)

        printClustersProbabilities(apn)
        
    f.close()

    if (pflowFile != 'null'):
        editPflow(apn, pflowFile)


def getArgs():
    # Program arguments
    parser = argparse.ArgumentParser(description='learning automata')
    parser.add_argument('jsonFile', type=str, nargs=1)
    parser.add_argument('-n', '--num', dest='fireNumber',
                        default=0, help='number of transistions to fire')
    parser.add_argument('-l', '--load_mod', action='store_true',
                        help='load net wih control places')
    parser.add_argument('-m', '--mod', dest='net_name', default='null',
                        help='net to modify')
    parser.add_argument('-r', '--rep', dest='repeat',
                        default=1, help='repeat complete execution')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='load net wih control places')

    return parser.parse_args()

def printClustersProbabilities(apn):
    print("\nCLUSTER PROBABILITY:\n")
    for cluster in apn.clusterManager.clusters:
        if(cluster.LA != None):
            printCluster(cluster)

    for cluster in apn.clusterManager.controlClusters:
        printCluster(cluster)

def printCluster(cluster):
    str_vector = ''
    for i in cluster.transitionList:
        str_vector += '{:>6}, '.format(i)
    str_vector = str_vector[:-2]
    print('\t[{}]'.format(str_vector))

    str_vector = ''
    for i in cluster.LA.probabilityVector.tolist():
        str_vector += '{:1.4f}, '.format(i)
    str_vector = str_vector[:-2]
    print('\t[{}]\n'.format(str_vector))

def writeResults(f, apn):
    for cluster in apn.clusterManager.clusters:
        if(cluster.LA != None):
            f.write(np.array2string(cluster.LA.probabilityVector))
    for cluster in apn.clusterManager.controlClusters:
        if(cluster.LA != None):
            f.write(np.array2string(cluster.LA.probabilityVector))
    f.write('\n')

def editPflow(apn, pflowFile):
    petriShape = editor.obtain_elements(
            apn.rdp.iPlusMatrix, apn.rdp.iMinusMatrix, apn.rdp.inhibitionMatrix, apn.rdp.initialMarking)

    newTransitions = petriShape.transitions[-(len(apn.rdp.updateT)-1):]
    newPlaces = petriShape.places[-len(newTransitions)*2:]
    newArcs = []

    for arc in petriShape.arcs:
        for place in newPlaces:
            if arc.srcId == place.label or arc.dstId == place.label:
                newArcs.append(arc)

    editor.modify_net(pflowFile, newPlaces, newTransitions, newArcs)

if __name__ == "__main__":
    main()
