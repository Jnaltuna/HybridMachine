import json
import numpy as np


class Rdp:

    FILENAME = "petrinet.json"

    def __init__(self, loadModified):
        self.updateT = []
        self.conflictList = []
        self.iMatrix = []
        self.iPlusMatrix = []
        self.iMinusMatrix = []
        self.inhibitionMatrix = []
        self.costVector = []
        self.marking = []
        self.initFromFile(self.FILENAME)
        self.clusterlist = self.defineClusterList(self.conflictList)

    def initFromFile(self, fileName):
        json_file = open(fileName, "r")
        json_data = json.load(json_file)
        json_file.close()

        self.conflictList = json_data["Conflictos"]
        self.updateT = json_data["UpdateT"]
        self.iMatrix = np.array(json_data["Incidencia"])
        self.iPlusMatrix = np.array(json_data["I+"])
        self.iMinusMatrix = np.array(json_data["I-"])
        self.inhibitionMatrix = np.array(json_data["Inhibicion"])
        self.costVector = np.array(json_data["Costos"])
        self.marking = np.array(json_data["Marcado"])

    def getUpdateT(self):
        updateT = [None]
        for x in self.updateT:
            transition = int(x.replace('T', '')) - 1
            updateT.append(transition)
        return updateT

    def defineClusterList(self, conflicts):

        tempList = []
        for x in conflicts:
            tempList.append(x[1])

        conflictList = []
        usedTransitions = []
        for x in tempList:
            a = []
            for y in x:
                transition = int(y.replace('T', '')) - 1
                a.append(transition)
                usedTransitions.append(transition)
            conflictList.append(a)

        numT = self.iMatrix.shape[1]
        a = []
        for T in range(numT):
            if usedTransitions.count(T) == 0:
                a.append(T)
        conflictList.insert(0, a)
        return conflictList

    def modifyNet(self):  # TODO
        # define conflicts and add places/transitions
        print('')

    def calcularSensibilizadas(self):

        # Marking restrictions

        T = self.iMinusMatrix.transpose()
        enabled = np.full(len(T), True)

        for row in range(len(T)):
            for i in range(len(T[row])):
                if(self.marking[i] < T[row][i]):
                    enabled[row] = False
                    break

        # Inhibition restrictions
        T = self.inhibitionMatrix.transpose()

        for row in range(len(T)):
            for i in range(len(T[row])):
                if(T[row][i] != 0 and T[row][i] < self.marking[i]):
                    enabled[row] = False
                    break

        return enabled

    def fire(self, numTransicion):
        self.marking = self.marking + \
            self.iMatrix[:, numTransicion]
        return self.costVector[numTransicion]
