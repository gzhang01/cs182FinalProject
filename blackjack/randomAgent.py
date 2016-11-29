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
from automatedAgent import AutomatedAgent

import random

# RandomAgent inherits from AutomatedAgent, overwriting chooseBet and 
# chooseAction methods to play randomly
class RandomAgent(AutomatedAgent):
	# Returns random valid action
	def chooseAction(self, actions, dealerUpcard):
		# Pick random action
		choice = random.choice(actions.keys())
		if not self.noPrint: print actions[choice]
		return choice