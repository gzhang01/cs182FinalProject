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
import math

# Q-Learning Agent
# Represent state as player value, dealer value, whether hand is soft or not
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
        self.count = 0

        if "flags" in kwargs:
            if "-qtrain" in kwargs["flags"]:
                self.train = True
    
    def chooseBet(self, deck):
        bet = self.mitStrategy(deck)
        # Replenish money if almost out
        if self.money < 10:
            if self.train:
                self.money = const.startingMoney
                return bet
            else:
                return self.money
        elif self.train and 2 * bet > self.money:
            self.money = const.startingMoney
            if not self.noPrint: print bet
            return bet
        else:
            if not self.noPrint: print bet
            return bet

    # Returns constant bet if money allows, else all money
    def chooseUniformBet(self):
        # Replenish money if almost out
        if self.train and self.money < 2 * const.betValue:
            self.money = const.startingMoney
        bet = const.betValue if const.betValue < self.money else self.money
        if not self.noPrint: print bet
        return bet

    # Player's advantage increases by .5% for each true count
    def calculateAdvantage(self, deck):
        numDecks = math.ceil(deck.getNumCardsLeft() / 52.0)
        trueCount = self.count / numDecks
        return trueCount * 0.05

    # Uses the Kelly Criterion to determine bet: minimum if advantage non-positive
    # otherwise bet percentage of current bankroll according to advantage
    def kellyCriterion(self, deck):
        adv = self.calculateAdvantage(deck)
        if adv > 0:
            bet = int(self.money * adv)
            if bet < 10:
                return 10
            else:
                return bet
        else:
            # Assume minimum bet of $10
            return 10

    # Uses MIT strategy to bet: minimum if count 0 or less, bet = (count - 1)*unit else
    def mitStrategy(self, deck):
        numDecks = round(deck.getNumCardsLeft() / 52.0)
        trueCount = self.count / numDecks
        if trueCount - 1 >= 1:
            bet = int((trueCount - 1) * 10)
            if bet > self.money:
                bet = self.money
            return bet
        else:
            # Assume minimum bet of $10
            return 10

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
        self.qVals[(self.current, action)] = (1 - self.alpha) * oldValue + self.alpha * reward
        self.current = nextState

    def getPolicy(self, state, actions):
        return self.computeActionFromQValues(state, actions)

    def getValue(self, state, actions):
        return self.computeValueFromQValues(state, actions)

    def writeData(self):
        if not self.train:
            with open(self.file, "a") as f:
                f.write(str(self.money) + "\n")

    # Overriding updateCount
    def updateCount(self, playerHand, dealerHand):
        high = set(['A', 'K', 'Q', 'J', '10'])
        low = set(['2', '3', '4', '5', '6'])
        allCards = playerHand + dealerHand
        for c in allCards:
            if c.getValue() in high:
                self.count -= 1
            elif c.getValue() in low:
                self.count += 1

    def reshuffled(self):
        self.count = 0

    def setTraining(self, training):
        self.train = training

    def setMoney(self, money):
        self.money = money

# Unit tests for Basic Strategy Agent
class TestAgentMethods(unittest.TestCase):
    
    def setUp(self):
        self.player = QLearningAgent(0.8, 0.1, 1)

    def tearDown(self):
        self.player = None

    def test_updateCount(self):
        self.player.updateCount([Card('K', 'C')], [Card('Q', 'S')])
        self.assertEquals(self.player.count, -2)
        self.player.updateCount([Card('2', 'C'), Card('A', 'C'), Card('5', 'C')], [Card('Q', 'S'), Card('A', 'S')])
        self.assertEquals(self.player.count, -3)

    def test_kellyCriterion(self):
        deck = BlackjackDeck()
        deck.drawCard()
        self.player.updateCount([Card('2', 'C'), Card('3', 'C'), Card('5', 'C')], [Card('Q', 'S')])
        self.assertEquals(self.player.count, 2)
        self.assertEquals(self.player.calculateAdvantage(deck), 0.0125)
        self.assertEquals(self.player.kellyCriterion(deck), 12.5)

    def test_mitStrategy(self):
        deck = BlackjackDeck()
        deck.drawCard()
        self.player.updateCount([Card('2', 'C'), Card('3', 'C'), Card('5', 'C')], [Card('Q', 'S'), Card('4', 'S')])
        self.player.updateCount([Card('2', 'C'), Card('3', 'C'), Card('5', 'C')], [Card('Q', 'S'), Card('4', 'S')])
        self.player.updateCount([Card('2', 'C'), Card('3', 'C'), Card('5', 'C')], [Card('Q', 'S'), Card('4', 'S')])
        self.assertEquals(self.player.count, 9)
        self.assertEquals(self.player.mitStrategy(deck), 5)

# Run tests if run from terminal
if __name__ == "__main__":
    unittest.main()