####
 # qLearningAgent.py
 #
 # Q-Learning Agent for blackjack
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card 
from deck import BlackjackDeck
from automatedAgent import AutomatedAgent
import constants as const

import random
import unittest
import time

# Q-Learning Agent
# Represent state as player value, dealer value, (bet value)
# Reward corresponds to subsequent hand value (if not bust) and high negative reward
# if bust, high positive reward if win (which action does win correspond to?)
# TODO: Reward should scale with current bet. How to represent winnings?
class QLearningAgent(AutomatedAgent):

    def __init__(self, epsilon, alpha, discount, **kwargs):
        super(QLearningAgent, self).__init__(**kwargs)
        # Dictionary of state, action pairs as key, q-value as value
    	self.qVals = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount
        # Keep track of current state
        self.current = None
        # Is training
        self.train = False

        if "flags" in kwargs:
            if "-qtrain" in kwargs["flags"]:
                self.train = True
        
    # Returns constant bet if money allows, else all money
    def chooseBet(self):
        # Replenish money if almost out
        if self.train and self.money < 2 * const.betValue:
            self.money = const.startingMoney
        bet = const.betValue if const.betValue < self.money else self.money
        if not self.noPrint: print bet
        return bet

    def updateState(self, state):
        self.current = state
   
    # Return Q-Value given a state, action pair. Return 0.0 if state, action
    # pair never seen before
    def getQValue(self, state, action):
    	if (state, action) in self.qVals.keys():
        	return self.qVals[(state, action)]
        else:
        	return 0.0

    # Compute value of state from Q-Values
    def computeValueFromQValues(self, state, actions):
        # Returns max over actions of the q-values given state
        if len(actions) == 0: 
            return 0.0
        qVals = [self.getQValue(state, a) for a in actions]
        return max(qVals)

    # Return an action from a state
    def computeActionFromQValues(self, state, actions):
        if len(actions) == 0: 
            return None
        if len(actions) == 1:
            return 1
        qVals = [(a, self.getQValue(state, a)) for a in actions]
        bestActions = [qVals[0][0]]
        maxQVal = qVals[0][1]
        for i in xrange(1, len(qVals)):
            if qVals[i][1] > maxQVal:
                bestActions = [qVals[i][0]]
                maxQVal = qVals[i][1]
            elif qVals[i][1] == maxQVal:
                bestActions.append(qVals[i][0])
        return random.choice(bestActions)

    def chooseAction(self, actions, dealerUpcard):
        state = self.current
        # Pick Action
        if random.random() < self.epsilon:
            return random.choice(actions.keys())
        return self.getPolicy(state, actions)

    # Called by parent class (game) to update Q-Values
    def update(self, action, nextState, reward):
        # print self.current, action, nextState, reward
        # time.sleep(1)
        nextStateActions = self.getLegalActions(nextState[0])
        if reward == None:
            # if no reward passed in, reward is q-value of next state
            reward = self.computeValueFromQValues(nextState, nextStateActions)
        if (self.current, action) in self.qVals:
            oldValue = self.qVals[(self.current, action)]
        else:
            oldValue = 0.0
        self.qVals[(self.current, action)] = (1 - self.alpha) * oldValue + self.alpha * (reward + self.discount * self.getValue(nextState, nextStateActions))
        self.current = nextState

    def getPolicy(self, state, actions):
        return self.computeActionFromQValues(state, actions)

    def getValue(self, state, actions):
        return self.computeValueFromQValues(state, actions)

    def writeData(self):
        if not self.train:
            with open(self.file, "a") as f:
                f.write(str(self.money) + "\n")

    def setTraining(self, training):
        self.train = training

    def setMoney(self, money):
        self.money = money

# Unit tests for Basic Strategy Agent
class TestAgentMethods(unittest.TestCase):
    
    def setUp(self):
        self.player = QLearningAgent(0.1, 0.5, 0.2)

    def tearDown(self):
        self.player = None

    def test_update(self):
        # Player hand 16, dealer hand 9, action is hit
        self.player.update((16, 9), 1, (18, 9), 18)
        self.assertEquals(self.player.getValue((16, 9)), 9.0)

# Run tests if run from terminal
if __name__ == "__main__":
    unittest.main()