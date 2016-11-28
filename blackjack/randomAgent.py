####
 # randomAgent.py
 #
 # Agent that chooses to hit or stand randomly, bets uniformly
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

# RandomAgent inherits from Player, overwriting getBet and getAction methods
# to play randomly
class RandomAgent(Player):
	
	# Returns random bet from 0 to current amount available
	def getBet(self):
		if not self.noPrint:
			print "\n"
			print "Money: {0}".format(self.money)
			print "Bet: ",

		# bet = random.randint(0, self.money)
		bet = const.betValue
		self.money -= bet

		return bet

	# Returns random valid action
	def getAction(self):
		value = self.getHandValue()
		blackjack = True if value[0] == const.blackjack else False
		bust = False if blackjack else value[0] > 21

		if not self.noPrint:
			self.presentState(bust, blackjack, value)

		# Pick random action
		choice = random.randint(1, 2)

		# If bust or blackjack, return
		if bust or blackjack:
			return "bust" if bust else "stand" if blackjack else None

		# Else, present all possible choices
		elif choice in const.actions.keys():
			return const.actions[choice]