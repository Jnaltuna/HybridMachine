import numpy as np
import random

a = 0.2  # or 0.05
b = 0.005
#b = 0


class LearningAutomata:

    def __init__(self, transitionList):
        self.actionList = transitionList
        self.probabilityVector = np.full(
            len(transitionList), 1/len(transitionList))
        self.enabledActions = []
        self.scaledProbabilityVector = []
        self.K = 0
        self.firedAction = -1
        self.count = [0] * len(self.actionList)
        self.limit = 10
        #print("Actions", self.actionList)
        #print("Probability", self.probabilityVector)

    def update(self, beta):

        # If there's only one action it shouldn't update the probabilities
        # if(len(self.enabledActions) < 2):
        #    print('New Probability Vector!', self.probabilityVector)
        #    return
        if (self.firedAction not in self.actionList):
            return

        #if(self.probabilityVector[self.actionList.index(self.firedAction)] > 0.9 and beta == 0):
        #    return
        
        #if(self.probabilityVector[self.actionList.index(self.firedAction)] < 0.05 and beta == 1):
        #    return

        for action in self.actionList:
            actionIndex = self.actionList.index(action)
            previousProb = self.probabilityVector[actionIndex]
            if beta == 0:
                if action == self.firedAction:
                    newProb = previousProb + a * (1 - previousProb)
                else:
                    newProb = (1-a) * previousProb
            else:
                if action == self.firedAction:
                    newProb = (1-b) * previousProb
                else:
                    r = len(self.actionList)
                    newProb = (b/(r-1)) + (1 - b) * previousProb

            self.probabilityVector[self.actionList.index(
                action)] = newProb
            # * self.K

        #print('New Probability Vector!', self.probabilityVector)

    def execute(self, enabledActions):
        self.enabledActions = enabledActions
        # Escalado de probabilidades
        #print('Enabled T: ', enabledActions)
        for elem in self.count:
            transition = self.actionList[self.count.index(elem)]
            if (elem > self.limit and transition in enabledActions):
                print('Fired ',transition)
                self.firedAction = transition
                self.setCount(enabledActions)
                return self.firedAction

        K = 0

        for action in enabledActions:
            K += self.probabilityVector[self.actionList.index(action)]

        self.K = K

        scaledProbVector = np.empty(len(enabledActions))

        for i in range(len(scaledProbVector)):
            scaledProbVector[i] = self.probabilityVector[self.actionList.index(
                enabledActions[i])] / K
        self.scaledProbabilityVector = scaledProbVector
        #print('Scaled: ', scaledProbVector, 'K: ', K)

        self.firedAction = random.choices(
            enabledActions, scaledProbVector, k=1)[-1]

        self.setCount(enabledActions)

        return self.firedAction
    
    def setCount(self, enabledActions):
        for i in range(len(self.actionList)):
            if(self.actionList[i] in enabledActions):
                if(self.actionList[i] != self.firedAction):
                    self.count[i] += 1
                else:
                    self.count[i] = 0
