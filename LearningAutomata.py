import numpy as np
import random

a = 0.1  # or 0.05
b = 0.05


class LearningAutomata:

    def __init__(self, transitionList):
        self.actionList = transitionList
        self.probabilityVector = np.full(
            len(transitionList), 1/len(transitionList))
        self.enabledActions = []
        self.scaledProbabilityVector = []
        self.K = 0
        self.firedAction = 0
        print("Probability", self.probabilityVector)
        print("Actions", self.actionList)

    def update(self, beta):

        for action in self.enabledActions:
            actionIndex = self.enabledActions.index(action)
            previousProb = self.scaledProbabilityVector[actionIndex]
            if beta == 0:
                if action == self.firedAction:
                    newProb = previousProb + a * (1 - previousProb)
                else:
                    newProb = (1-a) * previousProb
            else:
                if action == self.firedAction:
                    newProb = (1-b) * previousProb
                else:
                    r = len(self.enabledActions)
                    newProb = (b/(r-1)) + (1 - b) * previousProb
            #self.scaledProbabilityVector[actionIndex] = newProb
            self.probabilityVector[self.actionList.index(
                action)] = newProb * self.K

        print('New Probability Vector!', self.probabilityVector)

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
        print('Scaled: ', scaledProbVector, 'K: ', K)

        self.firedAction = random.choices(
            enabledActions, scaledProbVector, k=1)[-1]

        return self.firedAction
