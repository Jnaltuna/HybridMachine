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
        self.nPlaces = 0
        self.nTransitions = 0
        self.initFromFile(self.FILENAME, loadModified)

        # if loadModified == False:
        self.modifyNet()
        self.clusterlist = self.defineClusterList(self.conflictList)

    def initFromFile(self, fileName, loadModified):
        json_file = open(fileName, "r")
        json_data = json.load(json_file)
        json_file.close()

        if loadModified == True:
            self.conflictList = json_data["Conflictos"]
            self.updateT = json_data["UpdateT"]
        self.iMatrix = np.array(json_data["Incidencia"])
        self.iPlusMatrix = np.array(json_data["I+"])
        self.iMinusMatrix = np.array(json_data["I-"])
        self.inhibitionMatrix = np.array(json_data["Inhibicion"])
        self.costVector = np.array(json_data["Costos"])
        self.marking = np.array(json_data["Marcado"])

        self.nPlaces = self.iMatrix.shape[0]
        self.nTransitions = self.iMatrix.shape[1]

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
        initConflicts = self.identifyConflicts()
        finalConflicts = self.joinConflicts(initConflicts)

        #conflictList = []
        # for row in finalConflicts:
        #    conflict = []
        #    for i in range(len(row)):
        #        if row[i] > 0:
        #            conflict.append(i)
        #    conflictList.append(conflict)
        #self.conflictList = conflictList
        print('Conflict', finalConflicts)

    def identifyConflicts(self):

        conflictMatrix = []
        for row in self.iMinusMatrix:
            conflict = []
            for t in range(len(row)):
                if (row[t] > 0):
                    conflict.append(t)
            if (len(conflict) > 1):
                conflictRow = [0] * self.nTransitions
                for t in conflict:
                    conflictRow[t] = 1
                conflictMatrix.append(conflictRow)
                # conflictMatrix.append(conflict)

        # return conflictMatrix
        return np.asarray(conflictMatrix)

    def joinConflicts(self, conflictMatrix):

        for i in range(self.nTransitions):
            shared = []
            column = conflictMatrix[:, i]
            for j in range(len(column)):
                if(column[j] > 0):
                    shared.append(j)
            if(len(shared) > 1):
                for row in range(1, len(shared)):
                    conflictMatrix[shared[0]] = conflictMatrix[shared[0]
                                                               ] + conflictMatrix[shared[row]]
                    conflictMatrix = np.delete(
                        conflictMatrix, shared[row], axis=0)

        # conflicts = []
        # for i in range(len(conflictMatrix)):
        #     for j in range(len(conflictMatrix)):
        #         if i != j:
        #             for element in conflictMatrix[i]:
        #                 if element in conflictMatrix[j]:
        #                     # conflictMatrix[i] = conflictMatrix[i] + \
        #                     #    list(
        #                     #        set(conflictMatrix[j]) - set(conflictMatrix[i]))
        #                     conflicts.append(conflictMatrix[i] + list(
        #                         set(conflictMatrix[j]) - set(conflictMatrix[i])))
        # print('joined: ', conflicts)

        potentialConflicts = []
        for row in conflictMatrix:
            conflict = []
            for i in range(len(row)):
                if(row[i] > 0):
                    conflict.append('T' + str(i+1))
            potentialConflicts.append(conflict)

        return potentialConflicts

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
