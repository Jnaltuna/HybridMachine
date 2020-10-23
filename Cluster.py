from LearningAutomata import LearningAutomata


class Cluster:

    def __init__(self, automata, transitionList, updateT):
        self.updateT = updateT
        self.transitionList = transitionList
        self.LA = automata

        self.cost = 0
        self.historic = []
        self.meanCost = 0

    def updateLA(self):

        self.historic.append(self.cost)
        #self.historic.append(self.cost)
        self.meanCost = self.meanCost + \
            (self.cost - self.meanCost) / len(self.historic)

        if(self.cost < self.meanCost):
            beta = 0
        else:
            beta = 1

        self.LA.update(beta)

        self.cost = 0

        return

    def executeLA(self, enabledActions):
        fireT = self.LA.execute(enabledActions)
        return fireT
