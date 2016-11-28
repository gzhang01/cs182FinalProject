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
from player import Player 
import constants as const

import random
import unittest

# Q-Learning Agent
# Represent state as player value, dealer value, (bet value)
# Reward corresponds to subsequent hand value (if not bust) and high negative reward
# if bust, high positive reward if win (which action does win correspond to?)
# TODO: Reward should scale with current bet. How to represent winnings?
class QLearningAgent(Player):
    
	def __init__(self, noPrint=False, money=1000):
        super(QLearningAgent, self).__init__(noPrint, money)
        # Dictionary of state, action pairs as key, q-value as value
    	self.qVals = {}

    # Return Q-Value given a state, action pair. Return 0.0 if state, action
    # pair never seen before
    def getQValue(self, state, action):
    	if (state, action) in self.qVals:
        	return self.qVals[(state, action)]
        else:
        	return 0.0

    # Compute value of state from Q-Values
    def computeValueFromQValues(self, state):
        # Returns max over actions of the q-values given state
        legalActions = self.getLegalActions(state)
        if len(lega
        qVals =lActions) == 0: return 0.0 [self.getQValue(state, a) for a in legalActions]
        return max(qVals)

    # Return an action from a state
    def computeActionFromQValues(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0: return None
        qVals = [self.getQValue(state, a) for a in legalActions]
        bestActions = [legalActions[i] for i in xrange(len(legalActions)) if qVals[i] == max(qVals)]
        return random.choice(bestActions)

    def getAction(self, state):
        # Pick Action
        legalActions = self.getLegalActions(state)
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        return self.getPolicy(state)

    # Called by parent class (game) to update Q-Values
    def update(self, state, action, nextState, reward):
        self.qVals[(state, action)] = (1 - self.alpha) * self.qVals[(state, action)] + self.alpha * (reward + self.discount * self.getValue(nextState))

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)