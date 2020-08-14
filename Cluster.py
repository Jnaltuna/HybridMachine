from LearningAutomata import LearningAutomata


class Cluster:

    def __init__(self, transitionList, updateT):
        self.updateT = updateT
        self.transitionList = transitionList  # TODO view if neccesary
        self.LA = LearningAutomata(transitionList)
        self.cost = 0

    def updateLA(self):  # TODO
        # TODO llamar a update de LA
        print('holis')

    def executeLA(self):  # TODO
        print('')
