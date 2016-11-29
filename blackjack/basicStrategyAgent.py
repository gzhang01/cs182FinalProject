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

import random
import unittest

# This agent inherits from AutomatedAgent and implements the basic strategy for blackjack 
# to decide whether to hit or stand while betting randomly (where dealer stands on soft 17)
# Basic Strategy from: http://wizardofodds.com/games/blackjack/strategy/calculator/
class BasicStrategyAgent(AutomatedAgent):
	# Initalizes player, generates basic strategy dictionary
	def __init__(self, noPrint=False, money=100):
		super(BasicStrategyAgent, self).__init__(noPrint, money)
		self.strategy = {}
		self.generateStrategy()

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
