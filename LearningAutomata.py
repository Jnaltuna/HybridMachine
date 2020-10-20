import numpy as np
import random

a = 0.1  # or 0.05
b = 0.05
#b = 0


class LearningAutomata:

    def __init__(self, transitionList):
        self.actionList = transitionList
        self.probabilityVector = np.full(
            len(transitionList), 1/len(transitionList))
        self.enabledActions = []
        self.scaledProbabilityVector = []
        self.K = 0
        self.firedAction = 0
        #print("Actions", self.actionList)
        #print("Probability", self.probabilityVector)

    def update(self, beta):

        # If there's only one action it shouldn't update the probabilities
        # if(len(self.enabledActions) < 2):
        #    print('New Probability Vector!', self.probabilityVector)
        #    return
        if (self.firedAction not in self.actionList):
            return

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

        return self.firedAction
