####
 # basicStrategyAgent.py
 #
 # Agent that chooses to hit or stand according to basic strategy
 # Bets uniformly.
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card 
from deck import BlackjackDeck
import constants as const
from automatedAgent import AutomatedAgent
import math

import random
import unittest

# This agent inherits from AutomatedAgent and implements the basic strategy for blackjack 
# to decide whether to hit or stand while betting randomly (where dealer stands on soft 17)
# Basic Strategy from: http://wizardofodds.com/games/blackjack/strategy/calculator/
class BasicStrategyAgent(AutomatedAgent):
    # Initalizes player, generates basic strategy dictionary
    def __init__(self, **kwargs):
        super(BasicStrategyAgent, self).__init__(**kwargs)
        self.strategy = {}
        self.generateStrategy()
        self.doubleStrategy = {}
        self.generateDoubleStrategy()

    # Creates dictionary with (isSoft (bool), dealerValue, playerValue) tuple as key, 
    # action (1 is hit, 2 is stand) as value to encode basic strategy
    def generateStrategy(self):
        # Add 'hard' strategies
        for i in xrange(2, 12):
            for j in xrange(4, 22):
                # Player should stand in this range
                if (j == 12 and i >= 4 and i <= 6) or (j >= 13 and j<= 16 and i <= 6) or j >= 17:
                    self.strategy[(False, i, j)] = 2
                # Hit otherwise
                else:
                    self.strategy[(False, i, j)] = 1

        # Add 'soft' strategies
        for i in xrange(2, 12):
            for j in xrange(12, 22):
                # Stand in this range
                if j >= 19 or (j == 18 and i <= 8):
                    self.strategy[(True, i, j)] = 2
                # Hit otherwise
                else:
                    self.strategy[(True, i, j)] = 1
    
    # Creates dictionary with (isSoft (bool), dealerValue, playerValue) tuple as key, 
    # action (1 is hit, 2 is stand, 3 is double) as value to encode basic strategy
    def generateDoubleStrategy(self):
        # Add 'hard' strategies
        # Player should hit in this range
        for i in xrange(2, 12):
            for j in xrange(4, 9):
                self.strategy[(False, i, j)] = 1
        # Players should either double or hit in this range
        for i in xrange(2, 12):
            for j in xrange(9, 12):
                if j == 9:
                    if (i >= 3 and i <= 6):
                        self.strategy[(False, i, j)] = 3
                    else:
                        self.strategy[(False, i, j)] = 1
                elif j == 10:
                    if (i <= 9):
                        self.strategy[(False, i, j)] = 3
                    else:
                        self.strategy[(False, i, j)] = 1
                else:
                    if (i <= 10):
                        self.strategy[(False, i, j)] = 3
                    else:
                        self.strategy[(False, i, j)] = 1
        for i in xrange(2, 12):
            for j in xrange(12, 22):
                if j == 12:
                    if (i >= 4 and i <= 6):
                        self.strategy[(False, i, j)] = 2
                    else:
                        self.strategy[(False, i, j)] = 1
                elif j < 17:
                    if i >= 7:
                        self.strategy[(False, i, j)] = 1
                    else:
                        self.strategy[(False, i, j)] = 2
                # Always stand in this range
                else:
                    self.strategy[(False, i, j)] = 2

        # Add 'soft' strategies
        for i in xrange(2, 12):
            if (i == 5 or i == 6):
                self.strategy[(True, i, 12)] = 3
                self.strategy[(True, i, 13)] = 3
                self.strategy[(True, i, 14)] = 3
            else:
                self.strategy[(True, i, 12)] = 1
                self.strategy[(True, i, 13)] = 1
                self.strategy[(True, i, 14)] = 1
        for i in xrange(2, 12):
            if (i >= 4 and i <= 6):
                self.strategy[(True, i, 15)] = 3
                self.strategy[(True, i, 16)] = 3
            else:
                self.strategy[(True, i, 15)] = 1
                self.strategy[(True, i, 16)] = 1
        for i in xrange(2, 12):
            if (i >= 3 and i <= 6):
                self.strategy[(True, i, 17)] = 3
            else:
                self.strategy[(True, i, 17)] = 1
        for i in xrange(2, 12):
            if (i == 2 or i == 7 or i == 8):
                self.strategy[(True, i, 18)] = 2
            elif (i >= 3 and i <= 6):
                self.strategy[(True, i, 18)] = 3
            else:
                self.strategy[(True, i, 18)] = 1
        for i in xrange(2, 12):
            for j in xrange(19, 22):
                self.strategy[(True, i, j)] = 2

    # Returns action according to dealer's value and basic strategy
    def chooseAction(self, actions, dealerUpcard):
        # If length of actions is 1, then must be OK case (bust / blackjack)
        # Otherwise, there will be at least two actions (hit / stand)
        if len(actions) == 1:
            return actions.keys()[0]
        
        # Actions should never be empty!
        if len(actions) < 1:
            raise RuntimeError("Actions should not be empty!")

        # Otherwise, look at strategy
        value = self.getHandValue()
        choice = self.strategy[(value[1], self.getCardValue(dealerUpcard), value[0])]
        if not self.noPrint: print actions[choice]
        return choice

    # Initalizes player, generates basic strategy dictionary
    def __init__(self, **kwargs):
        super(BasicStrategyAgent, self).__init__(**kwargs)
        self.strategy = {}
        self.generateStrategy()
        self.count = 0

    def chooseBet(self, deck):
        bet = self.chooseUniformBet(deck)
        if self.money < 10:
            return self.money
        else:
            if not self.noPrint: print bet
            return bet

    # Returns constant bet if money allows, else all money
    def chooseUniformBet(self, deck):
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

# Unit tests for Basic Strategy Agent
class TestAgentMethods(unittest.TestCase):
    
    def setUp(self):
        self.player = BasicStrategyAgent()

    def tearDown(self):
        self.player = None

    def test_generateStrategy(self):
        self.player.generateStrategy()
        self.assertEqual(self.player.strategy[(False, 5, 8)], 1)
        self.assertEqual(self.player.strategy[(False, 6, 12)], 2)
        self.assertEqual(self.player.strategy[(False, 11, 21)], 2)
        self.assertEqual(self.player.strategy[True, 10, 13], 1)
        self.assertEqual(self.player.strategy[True, 6, 18], 2)
        self.assertEqual(self.player.strategy[True, 10, 20], 2)

# Run tests if run from terminal
if __name__ == "__main__":
    unittest.main()
