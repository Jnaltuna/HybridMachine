from Rdp import Rdp
from ClusterManager import ClusterManager
import numpy as np
import re


class ApnLa:

    def __init__(self, jsonFile, loadModified):

        self.rdp = Rdp(jsonFile, loadModified)

        clusterList = self.rdp.clusterlist
        print('Cluster list: ')
        for x in range(len(clusterList)):
            print(clusterList[x])
        updateT = self.rdp.updateT
        self.clusterManager = ClusterManager(clusterList, updateT, jsonFile)

        # Definimos el string de invariantes para chequear con regex
        tinv = ';\n'.join(';'.join('%d' % x for x in y)
                          for y in self.rdp.tInvariants)

        self.invariantStr = "\n{0!s};\n".format(tinv)
        print('Invariantes: ', self.invariantStr)

        self.partialInvariants = []

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)
        print('Fired Transition:', fireTransition)
        # firedCost = self.rdp.fire(fireTransition)
        self.rdp.fire(fireTransition)

        self.invariantAnalysis(fireTransition)

        self.clusterManager.updateIfNecessary(fireTransition)

        # print(self.partialInvariants)
        #input("\nPress Enter to continue...\n")

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
                print('matcheado perri')
                pattern = '\\n(?:{}{};\\n)'.format(partInv, fireTransition)
                if(re.search(pattern, self.invariantStr)):
                    # TODO: remuevo parcial y actualizo costos
                    print('Completa maquina')
                    costo = self.rdp.calcularCosto(
                        '{}{}'.format(partInv, fireTransition))
                    self.clusterManager.updateCost(costo)
                    self.partialInvariants.remove(partInv)

                    break
                else:  # TODO: actualizo parcial
                    print('parcial tigre')
                    self.partialInvariants[self.partialInvariants.index(
                        partInv)] += '{};'.format(fireTransition)
                    break

            # for inv in self.rdp.tInvariants:
            # self.clusterManager.updateCost(firedCost)
        if(newPartial):
            self.partialInvariants.append('{};'.format(fireTransition))

    def switcharoo(self):
        self.rdp.costVector[0] = 10
