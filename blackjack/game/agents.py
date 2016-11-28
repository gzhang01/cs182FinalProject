####
 # agents.py
 #
 # Learning agents for blackjack
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

# RandomAgent inherits from Player, overwriting getBet and getAction methods
# to play randomly
class RandomAgent(Player):
	
	# Returns random bet from 0 to current amount available
	def getBet(self, noPrint):
		if not noPrint:
			print "\n"
			print "Money: {0}".format(self.money)
			print "Bet: ",

		bet = random.randint(0, self.money)
		self.money -= bet

		return bet

	# Print current game state to user
	def presentState(self, bust, blackjack, value):
		print "Hand: " + " ".join([str(card) for card in self.hand])
		print "Value: {0}".format(value[0]), 
		if bust:
			print " (BUST) ",
		if blackjack:
			print " (BLACKJACK) ",
		print "\n"
		print "Options:"
		if bust or blackjack:
			print "    1. OK"
		else:
			for k in const.actions:
				print "    {0}: {1}".format(k, const.actions[k])
		print ""
		print "Selection: ",

	# Returns random valid action
	def getAction(self, noPrint):
		value = self.getHandValue()
		blackjack = True if value[0] == const.blackjack else False
		bust = False if blackjack else value[0] > 21

		if not noPrint:
			self.presentState(bust, blackjack, value)

		choice = random.randint(0, 1)

		# If bust or blackjack, return
		if bust or blackjack:
			return "bust" if bust else "stand" if blackjack else None

		# Else, present all possible choices
		elif choice in const.actions.keys():
			return const.actions[choice]

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
			for j in xrange(13, 22):
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

	# Returns action according to basic strategy
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






