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
	def getBet(self, noPrint):
		if not noPrint:
			print "\n"
			print "Money: {0}".format(self.money)
			print "Bet: ",

		# bet = random.randint(0, self.money)
		bet = const.betValue
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

		# Pick random action
		choice = random.randint(1, 2)

		# If bust or blackjack, return
		if bust or blackjack:
			return "bust" if bust else "stand" if blackjack else None

		# Else, present all possible choices
		elif choice in const.actions.keys():
			return const.actions[choice]