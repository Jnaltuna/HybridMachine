from LearningAutomata import LearningAutomata


class Cluster:

    def __init__(self, automata, transitionList, updateT):
        self.updateT = updateT
        self.transitionList = transitionList
        self.LA = automata

    def updateLA(self, cost, meanCost):

        if(cost < meanCost):
            beta = 0
        else:
            beta = 1

        self.LA.update(beta)

        return

    def executeLA(self, enabledActions):
        fireT = self.LA.execute(enabledActions)
        return fireT

    def setLastTransition(self, transition):
        if(self.LA != None):
            self.LA.firedAction = transition