####
 # automatedAgent.py
 #
 # Base agent for automated gameplay
 # NOTE: this agent should never be run
 # Bets uniformly
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card 
from deck import BlackjackDeck
from player import Player 
import constants as const

# AutomatedAgent inherits from Player, overwriting chooseBet and 
# chooseAction methods to play randomly
class AutomatedAgent(Player):
	
	# Returns constant bet if money allows, else all money
	def chooseBet(self):
		bet = const.betValue if const.betValue < self.money else self.money
		if not self.noPrint: print bet
		return bet


	# Returns random valid action
	def chooseAction(self, actions):
		raise RuntimeError("Choose Action Not Implemented")