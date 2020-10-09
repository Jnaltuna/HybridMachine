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
        self.clusterManager = ClusterManager(clusterList, updateT)

        # Definimos el string de invariantes para chequear con regex
        tinv = ';\n'.join(';'.join('%d' % x for x in y)
                          for y in self.rdp.tInvariants)

        self.invariantStr = "\n{0!s};\n".format(tinv)

        self.partialInvariants = ["0;"]

    def fireNext(self):

        enabledT = self.rdp.calcularSensibilizadas()

        fireTransition = self.clusterManager.getFireTransition(enabledT)
        print('Fired Transition:', fireTransition)
        # firedCost = self.rdp.fire(fireTransition)
        self.rdp.fire(fireTransition)

        self.rdp.tInvariants

        for partInv in self.partialInvariants:
            #pattern = '\\n(?:{};{};)'.format(partInv, fireTransition)
            pattern = '\\n(?:{}{};)'.format(partInv, 1)

            match = re.search(pattern, self.invariantStr)
            if match:
                print('matcheado perri')
                pattern = '\\n(?:{}{};\\n)'.format(partInv, 1)
                if(re.search(pattern, self.invariantStr)):
                    print('Completa maquina')
                    # TODO: remuevo parcial y actualizo costos
                else:
                    print('parcial tigre')
                    # TODO: actualizo parcial
            else:
                print('casi')
                # TODO: nueva parcial

            # for inv in self.rdp.tInvariants:

            # self.clusterManager.updateCost(firedCost)

        self.clusterManager.updateIfNecessary(fireTransition)

        return

    def switcharoo(self):
        self.rdp.costVector[0] = 10
