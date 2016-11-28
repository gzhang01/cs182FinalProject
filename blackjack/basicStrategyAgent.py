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
from player import Player 
import constants as const
from randomAgent import RandomAgent

import random
import unittest

# This agent inherits from RandomAgent and implements the basic strategy for blackjack 
# to decide whether to hit or stand while betting randomly (where dealer stands on soft 17)
# Basic Strategy from: http://wizardofodds.com/games/blackjack/strategy/calculator/
class BasicStrategyAgent(RandomAgent):
	
	# Initalizes player, generates basic strategy dictionary
	def __init__(self, money=100):
		self.hand = []
		self.money = money
		self.strategy = {}
		self.generateStrategy()

	# Creates dictionary with is soft (bool), dealer value, player value tuple as key, 
	# action (1 is hit, 2 is stand) as value to encode basic strategy
	def generateStrategy(self):
		# Add 'hard' strategies
		for i in xrange(2, 12):
			for j in xrange(5, 22):
				# Player should stand in this range
				if (j == 12 and i >= 4 and i <= 6) or (j >= 13 and j<= 16 and i <= 6) or j >= 17:
					self.strategy[(False, i, j)] = 2
				# Hit otherwise
				else:
					self.strategy[(False, i, j)] = 1

		# Add 'soft' strategies
		for i in xrange(2, 12):
			for j in xrange(13, 22):
				# Stand in this range
				if j >= 19 or (j == 18 and i <= 8):
					self.strategy[(True, i, j)] = 2
				# Hit otherwise
				else:
					self.strategy[(True, i, j)] = 1

	# Returns bet from 0 to current amount available
	def getBet(self, noPrint):
		if not noPrint:
			print "\n"
			print "Money: {0}".format(self.money)
			print "Bet: ",

		bet = const.betValue
		self.money -= bet

		return bet

	# Returns action according to dealer's value and basic strategy
	def getAction(self, noPrint, dealerValue):
		value = self.getHandValue()
		blackjack = True if value[0] == const.blackjack else False
		bust = False if blackjack else value[0] > 21

		if not noPrint:
			self.presentState(bust, blackjack, value)

		choice = self.strategy[(value[0], dealerValue, value[1])]

		# If bust or blackjack, return
		if bust or blackjack:
			return "bust" if bust else "stand" if blackjack else None

		# Else, present all possible choices
		elif choice in const.actions.keys():
			return const.actions[choice]

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
