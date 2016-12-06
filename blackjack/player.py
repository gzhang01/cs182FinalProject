####
 # player.py
 #
 # Class definition of a blackjack player
 #
 # CS182 - Artificial Intelligence
 # Fall 2016
 # Final Project 
 ##

from card import Card
from deck import BlackjackDeck
import unittest
import constants as const

class Player(object):
    # Initalizes player
    def __init__(self, **kwargs):
        self.hand = []
        self.money = const.startingMoney
        self.noPrint = const.noPrint
        self.collectData = False
        self.file = "../data/default.csv"
        self.rounds = 0
        self.wins = 0

        if "flags" in kwargs:
            if "-np" in kwargs["flags"]:
                self.noPrint = True
            if "-cd" in kwargs["flags"]:
                self.collectData = True
        if "money" in kwargs:
            self.money = kwargs["money"]
        if "file" in kwargs:
            self.file = "../data/" + kwargs["file"] + ".csv"

        with open(self.file, "w") as f:
            pass

    # Adds cards to hand
    def addToHand(self, *cards):
        for card in cards:
            assert (isinstance(card, Card))
            self.hand.append(card)

    # Returns hand as a list
    def getHand(self):
        return self.hand

    # Removes all cards from hand
    def discardHand(self):
        self.hand = []

    # Gets number of cards in hand
    def getNumCardsHeld(self):
        return len(self.hand)

    # Adds amount to money
    def addMoney(self, amount):
        self.money += amount

    # Returns amount of money player has
    def getMoney(self):
        return self.money

    # Gets the value of a card in blackjack
    def getCardValue(self, card):
        cardValue = card.getValue()
        if cardValue == 'A':
            return 11
        elif cardValue in ['K', 'Q', 'J']:
            return 10
        elif cardValue in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            return int(cardValue)
        else:
            raise ValueError("Card value {0} not recognized".format(cardValue))

    # Returns tuple (value, isSoft) denoting value of hand
    # If hand is blackjack, returns const.blackjack
    def getHandValue(self):
        # Counters for value and number of aces
        value = 0
        numAces = 0

        # Values of cards in hand
        cardValues = [card.getValue() for card in self.hand]

        # Checks for blackjack
        if self.getNumCardsHeld() == 2:
            if 'A' in cardValues and (len(set(['K', 'Q', 'J', '10']) & set(cardValues)) != 0):
                return (const.blackjack, False)

        # Find value for each card in hand
        for card in self.hand:
            cardValue = self.getCardValue(card)
            if cardValue == 11:
                numAces += 1
            value += cardValue

        # If over but have aces, change ace value to 1
        while value > 21 and numAces > 0:
            value -= 10
            numAces -= 1

        # Return (value, isSoft)
        return (value, numAces > 0)

    def validateBet(self, bet):
        return bet > 0 and bet <= self.money

    # Gets bet from user
    # If out of money, return False
    def getBet(self):
        if self.money <= 0:
            self.winRate = 100.0 * self.wins / self.rounds
            if not self.noPrint: print "Win rate: {0:.2f}%".format(self.winRate)
            return False

        if not self.noPrint:
            print "\n"
            print "Money: {0}".format(self.money)
            print "Bet: ",

        while True:
            bet = self.chooseBet()
            if self.validateBet(bet):
                self.money -= bet
                return bet
            print "Invalid Bet"
        

    # Agents chooses bet
    # Override this in subclasses
    def chooseBet(self):
        while True:
            bet = raw_input()
            try:
                bet = int(bet)
            except ValueError:
                print "Invalid Bet"
                continue

            return bet

    # Print current game state to user
    def presentState(self, bust, blackjack, value, actions):
        print "Hand: " + " ".join([str(card) for card in self.hand])
        print "Value: {0}".format(value[0]), 
        if bust:
            print " (BUST) ",
        if blackjack:
            print " (BLACKJACK) ",
        print "\n"
        print "Options:"
        for k in actions:
            print "    {0}: {1}".format(k, actions[k])
        print ""
        print "Selection: ",

    def getLegalActions(self, value):
        blackjack = True if value[0] == const.blackjack else False
        bust = False if blackjack else value[0] > 21

        if bust or blackjack:
            return {1: "OK"}
        else:
            return {
                1: const.actions[1],
                2: const.actions[2]
            }

    # Gets action from user
    def getAction(self, dealerUpcard):
        actions = self.getLegalActions(self.getHandValue())
        value = self.getHandValue()
        blackjack = True if value[0] == const.blackjack else False
        bust = False if blackjack else value[0] > 21

        if bust or blackjack:
            actions = {1: "OK"}

        if not self.noPrint:
            self.presentState(bust, blackjack, value, actions)

        while True:
            choice = self.chooseAction(actions, dealerUpcard)
            action = ""

            # If bust or blackjack, only allow one choice, and return
            if bust or blackjack:
                if choice == 1:
                    action = "bust" if bust else "stand" if blackjack else None
                else:
                    print "CHOICE", choice
                    print "Invalid choice"
                    continue
            # Else, present all possible choices
            elif choice in actions.keys():
                action = actions[choice]
            else:
                print choice
                print "Invalid choice"
                continue

            return action

    # Agent chooses action
    def chooseAction(self, actions, dealerUpcard):
        while True:
            choice = raw_input()
            try:
                choice = int(choice)
            except ValueError:
                print "Invalid choice"
                continue

            return choice

    # Writes data to file
    # Currently writes only amount of money
    def writeData(self):
        with open(self.file, "a") as f:
            f.write(str(self.money) + "\n")

    # Update count does nothing for normal players
    # Override in qLearningAgent
    def updateCount(self, playerHand, dealerHand):
        pass

    # Reshuffling notice
    # Override in qLearningAgent
    def reshuffled(self):
        pass

    # Actions to take when a round ends
    def roundEnd(self, reward, playerHand, dealerHand):
        if self.collectData: 
            self.writeData()

        # Updates the count
        self.updateCount(playerHand, dealerHand)

        self.rounds += 1
        if reward > 0:
            self.wins += 1

# Unit tests for Player class
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def tearDown(self):
        self.player = None

    def test_addToHand(self):
        self.player.addToHand(Card('10', 'S'))
        self.player.addToHand(Card('2', 'D'))
        with self.assertRaises(AssertionError):
            self.player.addToHand("foo")

    def test_getHand(self):
        cards = [Card('10', 'S'), Card('2', 'D')]
        self.player.addToHand(*cards)
        self.assertEqual(self.player.getHand(), cards)

    def test_getNumCardsHeld(self):
        self.player.addToHand(Card('10', 'S'))
        self.assertEqual(self.player.getNumCardsHeld(), 1)
        self.player.addToHand(Card('2', 'D'))
        self.assertEqual(self.player.getNumCardsHeld(), 2)

    def test_discardHand(self):
        self.player.addToHand(Card('10', 'S'))
        self.player.addToHand(Card('2', 'D'))
        self.assertEqual(self.player.getNumCardsHeld(), 2)
        self.player.discardHand()
        self.assertEqual(self.player.getNumCardsHeld(), 0)

    def test_getMoney(self):
        self.assertEqual(self.player.getMoney(), 100)

    def test_addMoney(self):
        self.player.addMoney(50)
        self.assertEqual(self.player.getMoney(), 150)

    def test_getHandValue(self):
        # Test blackjack cases
        for v in ['K', 'Q', 'J', '10']:
            self.player.addToHand(Card('A', 'S'), Card(v, 'D'))
            self.assertEqual(self.player.getHandValue()[0], const.blackjack)
            self.player.discardHand()

        # Hand value 21, not blackjack
        self.player.addToHand(Card('A', 'S'), Card('2', 'D'), Card('8', 'H'))
        self.assertEqual(self.player.getHandValue(), (21, True))
        self.player.discardHand()       
        self.player.addToHand(Card('10', 'S'), Card('3', 'D'), Card('8', 'H'))
        self.assertEqual(self.player.getHandValue(), (21, False))
        self.player.discardHand()

        # Ace needs to take on lower value
        self.player.addToHand(Card('A', 'S'), Card('9', 'D'), Card('A', 'H'))
        self.assertEqual(self.player.getHandValue(), (21, True))
        self.player.discardHand()
        self.player.addToHand(Card('A', 'S'), Card('2', 'D'), Card('9', 'H'))
        self.assertEqual(self.player.getHandValue(), (12, False))
        self.player.discardHand()

        # Make sure value is not restricted (i.e. can go above 21)
        self.player.addToHand(Card('10', 'S'), Card('6', 'D'), Card('8', 'H'))
        self.assertEqual(self.player.getHandValue(), (24, False))
        self.player.discardHand()


# Run tests if run from terminal
if __name__ == "__main__":
    unittest.main()