import json


class Rdp:

    FILENAME = "petrinet.json"

    def __init__(self, loadModified):
        self.updateT = []
        self.conflictList = []
        self.iMatrix = []
        self.iPlusMatrix = []
        self.iMinusMatrix = []
        self.inhibitionMatrix = []
        self.costsMatrix = []
        self.marking = []
        self.initFromFile(self.FILENAME)
        self.clusterlist = self.defineClusterList(self.conflictList)

    def initFromFile(self, fileName):
        json_file = open(fileName, "r")
        json_data = json.load(json_file)
        # json_file.close()

        self.conflictList = json_data["Conflictos"]
        self.updateT = json_data["UpdateT"]
        self.iMatrix = json_data["Incidencia"]
        self.iPlusMatrix = json_data["I+"]
        self.iMinusMatrix = json_data["I-"]
        self.inhibitionMatrix = json_data["Inhibicion"]
        self.costsMatrix = json_data["Costos"]
        self.marking = json_data["Marcado"]

    def getUpdateT(self, json_data):
        return

    def defineClusterList(self, conflicts):
        # create cluster list based on conflicts
        clusterList = []
        clusterList.append([])
        for x in conflicts:
            clusterList.append([])
        print(clusterList)

    def modifyNet(self):
        # define conflicts and add places/transitions
        print('')
