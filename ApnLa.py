from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np
import re


class ApnLa:

    def __init__(self, jsonFile, loadModified):

        self.rdp = Rdp(jsonFile, loadModified)

        clusterList = self.rdp.clusterlist
        
        updateT = self.rdp.updateT
        self.clusterManager = ClusterManager(
            clusterList, updateT, self.rdp.controlConflicts, self.rdp.tInvariants)

        # Definimos el string de invariantes para chequear con regex
        tinv = ';\n'.join(';'.join('%d' % x for x in y)
                          for y in self.rdp.tInvariants)

        self.invariantStr = "\n{0!s};\n".format(tinv)

        self.partialInvariants = []

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)

        self.rdp.fire(fireTransition)

        self.invariantAnalysis(fireTransition)

        self.clusterManager.setClusterFiredTransition(fireTransition)

        self.clusterManager.updateIfNecessary(fireTransition)

        return

    def invariantAnalysis(self, fireTransition):

        if(self.clusterManager.isUpdate(fireTransition)):
            return

        newPartial = True

        for partInv in self.partialInvariants:
            pattern = '\\n(?:{}{};)'.format(partInv, fireTransition)

            match = re.search(pattern, self.invariantStr)
            if match:
                newPartial = False
                pattern = '\\n(?:{}{};\\n)'.format(partInv, fireTransition)
                if(re.search(pattern, self.invariantStr)):

                    costo, invNum = self.rdp.calcularCosto(
                        '{}{}'.format(partInv, fireTransition))

                    self.clusterManager.updateCost(costo, invNum)

                    self.partialInvariants.remove(partInv)
                    break
                else:
                    self.partialInvariants[self.partialInvariants.index(
                        partInv)] += '{};'.format(fireTransition)
                    break

        if(newPartial):
            self.partialInvariants.append('{};'.format(fireTransition))

    def switcharoo(self):
        #self.rdp.costVector[0] = 50
        self.rdp.costVector[6] = 50
        self.rdp.costVector[4] = 25
        print(self.rdp.costVector)

    def printClusters(self):
        print("\nCLUSTERS:\n")
        print("\tRegular clusters")
        for cluster in self.clusterManager.clusters:
            print('\t\t*',cluster.transitionList)
        if (len(self.clusterManager.controlClusters) > 0):
            print("\tControl clusters")
            for cluster in self.clusterManager.controlClusters:
                print('\t\t*',cluster.transitionList)
