# # Blackjack - Beginning
# # Blackjack - Deck class
# # Blackjack - Card class
# # Blackjack - Hand class
# # Blackjack - Game class

import random

# ------------------------------------------------------------------------------
# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # Overload the 'print' function
    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

# ------------------------------------------------------------------------------
# Deck class
class Deck:
    def __init__(self):
        self.cards = []
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
                {"rank" : "A", "value" : 11},
                {"rank" : "2",  "value" : 2},
                {"rank" : "3",  "value" : 3},
                {"rank" : "4",  "value" : 4},
                {"rank" : "5",  "value" : 5},
                {"rank" : "6",  "value" : 6},
                {"rank" : "7",  "value" : 7},
                {"rank" : "8",  "value" : 8},
                {"rank" : "9",  "value" : 9},
                {"rank" : "10", "value" : 1}, 
                {"rank" : "J",  "value" : 10},
                {"rank" : "Q",  "value" : 10},
                {"rank" : "K",  "value" : 10},
                ]

        # Build the card deck with all 52 self.cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))     # Append cards as instances of the Card class

    # Function to shuffle the card deck
    def shuffle(self):
        if (len(self.cards) > 1):
            random.shuffle(self.cards)

    # Function to remove a card from the deck
    def deal(self, numberOfCards):
        cardsDealtList = []

        while (numberOfCards > 0):  # Using 'while' loop
            if (len(self.cards) > 0):
                card = self.cards.pop()
                cardsDealtList.append(card)
                numberOfCards -= 1
            # else:
            #     break

        return cardsDealtList


# ------------------------------------------------------------------------------
# Hand Class
class Hand:
    def __init__(self, dealer = False):
        self.cards = []
        self.value = 0
        self.dealer = dealer
        # dealer = True : means the Hand object is the computer dealer

    def addCard(self, cardList):
        self.cards.extend(cardList)

    def calculateValue(self):
        self.value = 0
        handHasAce = False

        for card in self.cards:
            cardValue = int(card.rank["value"])
            self.value += cardValue

            if ( card.rank["rank"] == "A"):
                handHasAce = True
        
        if ( (handHasAce) and (self.value > 21) ):
            self.value -= 10

    def getValue(self):
        self.calculateValue()
        return self.value
    
    def isBlackJack(self):
        return (self.value == 21)
    
    def display(self, showAllDealerCards = False):
        print(f'''{"Dealer's" if (self.dealer) else "Your"} Hand: ''')

        for cardIndex, card in enumerate(self.cards):
            if ( (cardIndex == 0) and (self.dealer) \
                and not(showAllDealerCards) and not(self.isBlackJack()) ):
                print("hidden")
            else: 
                print(card)

        if not(self.dealer):
            print(f"Value: {self.getValue()} \n") 


# ------------------------------------------------------------------------------
# Game Class
class Game:
    def play(self):
        gameNumber = 0
        gamesToPlay = 0

        while (gamesToPlay <= 0):
            try:
                gamesToPlay = int(input("How many games do you want to play?  "))
            except:
                print("You must enter a number! \n")

        
        while (gameNumber < gamesToPlay):
            gameNumber += 1

            deck = Deck()
            deck.shuffle()

            playerHand = Hand()
            dealerHand = Hand(dealer=True)
        
            for i in range(2):
                playerHand.addCard(deck.deal(1))
                dealerHand.addCard(deck.deal(1))
            
            print()
            print("*" * 30)
            print(f"Game {gameNumber} of {gamesToPlay}")
            print("*" * 30)
            playerHand.display()
            dealerHand.display()
            print()

            if ( self.checkWinner(playerHand, dealerHand) ):
                continue

            choice = ""
            while ( (playerHand.getValue() < 21) and ( choice not in ['s', 'stand'] ) ):
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()

                while (choice not in ['h', 's', 'hit', 'stand']):
                    choice = input("Please enter 'Hit' or 'Stand' (or 'H' / 'S'): ").lower()
                    print()
                
                if (choice in ['h', 'hit']):
                    playerHand.addCard(deck.deal(1))
                    playerHand.display()

            if ( self.checkWinner(playerHand, dealerHand) ):
                continue

            playerHandValue = playerHand.getValue()
            dealerHandValue = dealerHand.getValue()

            while (dealerHandValue < 17):
                dealerHand.addCard(deck.deal(1))
                dealerHandValue = dealerHand.getValue()
            
            dealerHand.display(showAllDealerCards=True)

            if ( self.checkWinner(playerHand, dealerHand) ):
                continue
        
            print()
            print("=" * 30)
            print("Final Results: ")
            print(f"Your hand: {playerHandValue}")
            print(f"Dealer's hand: {dealerHandValue}")
            print()

            self.checkWinner(playerHand, dealerHand, gameOver=True)

        print("\nThanks for playing!")


    def checkWinner(self, playerHand, dealerHand, gameOver = False):
        if not(gameOver):
            if (playerHand.getValue() > 21):
                print("You're busted. Dealer wins!")
                return True
            elif (dealerHand.getValue() > 21):
                print("Dealer busted. You win!")
                return True
            elif (playerHand.isBlackJack() and dealerHand.isBlackJack()):
                print("Both players have a BlackJack! Tie!")
                return True
            elif (playerHand.isBlackJack()):
                print("You have BlackJack! You win!")
                return True
            elif (dealerHand.isBlackJack()):
                print("Dealer has BlackJack! Dealer wins!")
                return True
        else:
            if (playerHand.getValue() > dealerHand.getValue()):
                print("You win!")
            elif (playerHand.getValue() == dealerHand.getValue()):
                print("Tie!")
            else:
                print("Dealer wins!")
            return True
        
        return False

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

newGame = Game()
newGame.play()