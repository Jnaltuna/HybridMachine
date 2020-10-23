import json
import numpy as np
import sys
from exceptions import NetException


class Rdp:

    FILENAME = "petrinet.json"
    #FILENAME = "PNunmodified.json"
    #FILENAME = "test.json"

    def __init__(self, jsonFile, loadModified):
        self.updateT = [None]
        self.conflictList = []
        self.iMatrix = []
        self.iPlusMatrix = []
        self.iMinusMatrix = []
        self.inhibitionMatrix = []
        self.costVector = []
        self.marking = []
        self.nPlaces = 0
        self.nTransitions = 0
        self.initFromFile(jsonFile, loadModified)

        if loadModified == False:
            self.modifyNet()

        self.initialMarking = np.copy(self.marking)
        self.clusterlist = self.defineClusterList(self.conflictList)

    def initFromFile(self, fileName, loadModified):
        json_file = open(fileName, "r")
        json_data = json.load(json_file)
        json_file.close()

        if loadModified == True:
            #self.conflictList = json_data["Conflictos"]
            #self.updateT = json_data["UpdateT"]
            conflictList = json_data["Conflictos"]
            updateT = json_data["UpdateT"]
            for conflict in conflictList:
                self.conflictList.append(self.parseTransitionsList(conflict))
            self.updateT.extend(self.parseTransitionsList(updateT))
            self.iMatrix = np.array(json_data["Incidencia"])

        self.iPlusMatrix = np.array(json_data["I+"])
        self.iMinusMatrix = np.array(json_data["I-"])
        self.inhibitionMatrix = np.array(json_data["Inhibicion"])
        self.costVector = np.array(json_data["Costos"])
        self.marking = np.array(json_data["Marcado"])

        self.nPlaces = self.iPlusMatrix.shape[0]
        self.nTransitions = self.iPlusMatrix.shape[1]

    def parseTransitionsList(self, tList):
        newtList = []
        for transition in tList:
            transition = int(transition.replace('T', '')) - 1
            newtList.append(transition)
        return newtList

    def defineClusterList(self, conflicts):  # TODO needs testings
        print('Conflicts', conflicts)
        usedTransitions = []
        for conflict in conflicts:
            usedTransitions.extend(conflict)

        clusterZ = []
        for T in range(self.nTransitions):
            if usedTransitions.count(T) == 0:
                clusterZ.append(T)
        conflictList = conflicts
        conflictList.insert(0, clusterZ)
        return conflictList

    def modifyNet(self):  # TODO
        # define conflicts and add places/transitions
        initConflicts = self.identifyConflicts()
        self.conflictList = self.joinConflicts(initConflicts)

        for conflict in self.conflictList:
            self.insertPlacesTransitions(conflict)

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
                deleteRows = []
                for row in range(1, len(shared)):
                    conflictMatrix[shared[0]] = conflictMatrix[shared[0]
                                                               ] + conflictMatrix[shared[row]]
                    deleteRows.append(shared[row])

                deleteRows.sort(reverse=True)
                for row in deleteRows:
                    conflictMatrix = np.delete(
                        conflictMatrix, row, axis=0)

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
                    conflict.append(i)
            potentialConflicts.append(conflict)

        return potentialConflicts

    def insertPlacesTransitions(self, conflict):

        # Para cada matriz -> 2 filas, 1 col. Marcado 2 col. Costo 1 col
        newIMinus = self.addRowsColumns(self.iMinusMatrix)
        newIPlus = self.addRowsColumns(self.iPlusMatrix)
        newInhibition = self.addRowsColumns(self.inhibitionMatrix)

        # Matriz I-
        # 1er fila, 1 en col de la T agregada
        newIMinus[-2, -1] = 1
        # 2da fila, 1 en col de las T del conflicto
        for T in conflict:
            newIMinus[-1, T] = 1

        # Matriz I+
        # 1er fila: plazas de entradas compartidas de las T del conflicto. Buscar T que entran a esas plazas.
        sharedPlaces = []
        for T in conflict:
            sharedPlaces.append(self.iMinusMatrix[:, T])

        prePlaces = np.ones(self.nPlaces)
        for i in range(len(sharedPlaces)):
            prePlaces = np.logical_and(prePlaces, sharedPlaces[i])

        input_transitions = np.zeros(self.nTransitions)
        for j in range(len(prePlaces)):
            if(prePlaces[j]):
                input_transitions = np.logical_or(
                    input_transitions, self.iPlusMatrix[j, :])
        newIPlus[-2, :-1] = input_transitions

        # 2da fila: 1 en col de las T agregada
        newIPlus[-1, -1] = 1

        # I: sumar ambas
        newIMatrix = newIPlus - newIMinus

        # Inhibicion:
        # 1er fila: todos ceros
        # 2da fila: 1 en col de la T agergada
        newInhibition[-1, -1] = 1

        # Marcado: 1 token en 2da col agregada si alguna plaza compartida tiene token
        prePlacesMarking = np.logical_and(prePlaces, self.marking)

        getsToken = np.isin(True, prePlacesMarking)
        newMarking = np.append(self.marking, [0, getsToken])

        # Cost
        newCost = np.append(self.costVector, 0)

        # Replacing
        self.iMinusMatrix = newIMinus
        self.iPlusMatrix = newIPlus
        self.iMatrix = newIMatrix
        self.inhibitionMatrix = newInhibition
        self.marking = newMarking
        self.costVector = newCost

        self.updateT.append(self.nTransitions)

        self.nPlaces += 2
        self.nTransitions += 1

        return

    def addRowsColumns(self, matrix):
        newMatrix = np.append(matrix, np.zeros(
            (self.nPlaces, 1)), axis=1)

        newMatrix = np.append(newMatrix, np.zeros(
            (2, self.nTransitions+1)), axis=0)
        return newMatrix

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
                if(T[row][i] != 0 and T[row][i] <= self.marking[i]):
                    enabled[row] = False
                    break

        if(np.count_nonzero(enabled) == 0):
            raise NetException("Red bloqueada")

        return enabled

    def fire(self, numTransicion):
        self.marking = self.marking + \
            self.iMatrix[:, numTransicion]
        return self.costVector[numTransicion]
