import random

rankings = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
suits = (u"\u2665", u"\u2660", u"\u2663", u"\u2666")

values = {'Two': 2,'Three': 3,'Four': 4,'Five': 5,'Six': 6,'Seven': 7,'Eight': 8,'Nine': 9,'Ten': 10,'Jack': 10,'Queen': 10,'King': 10,'Ace': 11}

playing = True



class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    #Method __str__ to convert into string
    def __str__(self):
        return self.rank + self.suit
#Creating the deck of cards
class Deck:
    def __init__(self):
        # Setting deck to an empty list
        self.deck = []
        for suit in suits:
            for rank in rankings:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_combination = ""
        for card in self.deck:
            # New line + a card is equal to dekck combination
            deck_combination += "\n" + card.__str__()
        return "The deck contains: " + deck_combination

    def shuffle_deck(self):
        #Method to shuffle cards in the deck
        random.shuffle(self.deck)

    def deal_card(self):
        #Picking a card from the end of the deck list which gets popped off.
        one_card = self.deck.pop()
        return one_card
    
class Hand:
    def __init__(self):
        self.cards = []
        #Keep track of card values
        self.value = 0
        #Keep track of number of aces
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        #Incrementing self.aces if card picked out is an ace
        if card.rank == 'Ace':
            self.aces += 1

    def choose_ace(self):
        while self.value > 21 and self.aces:
            #Making the ace a value of 1 instead of an 11 based on if the value of the player's hand is greater than 21
            self.value -= 10
            self.aces -= 1

class Bankroll():
    
    def __init__(self):
        self.total = 500
        self.bet = 0
    
    def win_game(self):
        self.total += self.bet
    
    def lose_game(self):
        self.total -= self.bet


#Creatiing our functions

#Check validity of the bet
def get_bet(bankroll):
    while True:
        bankroll.bet = int(input("\nPlace your bet: "))
        if bankroll.bet <= 0:
            print("The minimum bet is $1")
        elif bankroll.bet > bankroll.total:
            print("You do not have sufficient funds")
        else:
            break
#Create a funciton for hitting on dealer/player hand
def hit(deck, hand):
    hand.add_card(deck.deal_card())
    #Checking for ace
    hand.choose_ace()
#Ask for hit or stand
def hitorstand(deck, hand):
    #making playing avl in the function
    global playing

    while True:
        ask = input("\nWould you like to hit or stand? Enter 'h' for hit and 's' for stand. ")

        if ask.lower() == "h":
            hit(deck, hand)
        elif ask.lower() == "s":
            print("Player stands")
            # Stops player funciton while dealer can still play
            playing = False
        else:
            print("Sorry! Please type 'h' to hit and 's' for stand.")
            continue
        break

def show_partial(player, dealer):
    #Show first dealer card
    print("\nDealer's Hand: ")
    print(f"{dealer.cards[0]} and Unknown")
    print("\nPlayer's Hand: ")
    print("", *player.cards)


def show_hands(player, dealer):
    #Show all cards and points
    print("\nDealer's Hand: ", *dealer.cards, sep="\n ")
    print("Dealer's Value: ", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep="\n ")
    print("Player's Value: ", player.value)

#Game ending

def player_bust(player, dealer, bankroll):
    print("You have busted!")
    bankroll.lose_game()

def player_wins(player, dealer, bankroll):
    print("You have won!")
    bankroll.win_game()

def dealer_bust(player, dealer, bankroll):
    print("The dealer has busted!")
    bankroll.win_game()

def dealer_wins(player, dealer, bankroll):
    print("The dealer has won!")
    bankroll.lose_game()

def push(player, dealer):
    print("It's a push! The player and dealer have tied.")

#Designing Framework

while True:
    print("Thank you for playing Blackjack, let's start!")

    #shuffle and create deck
    deck = Deck()
    deck.shuffle_deck()

    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    #Keep track of player bankfroll
    player_bankroll = Bankroll()

    #Ask player for their bet
    get_bet(player_bankroll)

    #show cards for player and dealer
    show_partial(player_hand, dealer_hand)

    while playing:
        hitorstand(deck, player_hand)
        show_partial(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_bankroll)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        show_hands(player_hand, dealer_hand)

        if dealer_hand.value > 21:
                dealer_bust(player_hand, dealer_hand, player_bankroll)

        elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_bankroll)

        elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_bankroll)

        elif player_hand.value > 21:
                player_bust(player_hand, dealer_hand, player_bankroll)
        
    print("\nYour bankroll balance is: ", player_bankroll.total)

    new_game = input("\nWould you like to play another hand? ")

    if new_game.lower() == "yes" or new_game.lower() == "y":
        playing = True
        continue
    else:
        print("\nThank you for playing!")
        break