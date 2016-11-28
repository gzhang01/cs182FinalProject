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
	
	# Returns constant bet if money allows, else all money
	def chooseBet(self):
		bet = const.betValue if const.betValue < self.money else self.money
		if not self.noPrint: print bet
		return bet


	# Returns random valid action
	def chooseAction(self, actions):
		# Pick random action
		choice = random.choice(actions.keys())
		if not self.noPrint: print actions[choice]
		return choice