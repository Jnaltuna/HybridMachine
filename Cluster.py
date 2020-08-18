from LearningAutomata import LearningAutomata


class Cluster:

    def __init__(self, automata, transitionList, updateT):
        self.updateT = updateT
        self.transitionList = transitionList  # TODO view if neccesary
        self.LA = automata
        self.cost = 0

    def updateLA(self):  # TODO
        beta = 0

        # TODO define beta

        self.LA.update(beta)
        print('')

    def executeLA(self, enabledActions):  # TODO
        fireT = self.LA.execute(enabledActions)
        return fireT
