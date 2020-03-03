import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
	'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five:':5, 'Six':6, 'Seven':7, 'Eight':8,
 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#GAME ON VARIABLE
playing = True

#1.CREATING THE CARD CLASS
class Card():

 	def __init__(self, suit, rank):
 		self.suit = suit
 		self.rank = rank

 	#printing a 'card' object
 	def __str__(self):
 		return self.rank + ' of ' + self.suit

#2. CREATING THE DECK CLASS - store 52 card objects in a list that we can shuffle
class Deck():

	def __init__(self):
		self.deck = [] #start with an empty list

		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
			deck_comp += '\n' + card.__str__()
		return "The deck has: " + deck_comp

	#Method to shuffle the deck
	def shuffle(self):
		random.shuffle(self.deck)

	#Method to grab a card
	def deal(self):
		single_card = self.deck.pop()
		return single_card

#3. CREATING A HAND CLASS
class Hand():

	def __init__(self):
		self.cards = []    #start with empty list
		self.value = 0     #start with zero value
		self.aces = 0      #add an attrivute to keep track of aces

	def add_card(self, card):
		#card passed in is from Deck.deal() --> single Card(suit, rank)
		self.cards.append(card)
		self.value += values[card.rank]

		#track aces
		if card.rank == 'Ace':
			self.aces += 1

	def adjust_for_ace(self):
		#if total value > 21 and i still have an ace
		#then change my ace to be a 1 instead of an 11
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

#4. CHIPS CLASS
class Chips():

	def __init__(self, total = 100):
		self.total = total
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet

#5. FUNCTION FOR TAKING BETS
def take_bet(chips):

	while True:
		try:
			chips.bet = int(input("How many chips would you like to bet? "))
		except:
			print("Sorry, wrong bet. Try again!")
		else:
			if chips.bet > chips.total:
				print("Sorry, not enough chips. You have: {}. Try again.".format(chips.total))
			else:
				break

#6. FUNCTION FOR TAKING HITS
def hit(deck, hand):

	single_card = deck.deal()
	hand.add_card(single_card)
	hand.adjust_for_ace()		

#7. HIT OR STAND FUNCTION
def hit_or_stand(deck, hand):
	global playing

	while True:
		x = input('Hit or Stand? Enter h or s... ')
		if x[0].lower() == 'h':
			hit(deck, hand)
		elif x[0].lower() == 's':
			print("Player stands! Dealer's turn...")
			playing = True
		else:
			print("Sorry, I did not understand that. Please enter h or s only! ")
			continue

		break

#8. DISPLAY CARDS
def show_some(player, dealer):
	
	print("DEALERS HAND: ")
	print('HIDDEN CARD')
	print(dealer.cards[1])
	print('\n')
	print("PLAYERS HAND: ")
	for card in player.cards:
		print(card)
	print('\n')

def show_all(player, dealer):

	print("DEALERS HAND: ")
	for card in dealer.cards:
		print(card)
	print('\n')
	print("PLAYERS HAND: ")
	for card in player.cards:
		print(card)
	print('\n')

#9. END OF GAME SCENARIOS
def player_busts(player, dealer, chips):
	print('BUST PLAYER!')
	chips.lose_bet()

def player_wins(player, dealer, chips):
	print('PLAYER WINS!')
	chips.win_bet()

def dealer_busts(player, dealer, chips):
	print('PLAYER WINS! DEALER BUSTED!')
	chips.win_bet()

def dealer_wins(player, dealer, chips):
	print('DEALER WINS!')
	chips.lose_bet()

def push(player, dealer):
	print('Dealer and player tie! PUSH')

#10. THE GAME
while True:

	print("WELCOME TO BLACKJACK! ")

	#create and shuffle deck
	#deal 2 cards to each player
	deck = Deck()
	deck.shuffle()

	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	#set up player's chips
	player_chips = Chips()

	#prompt the first bet
	take_bet(player_chips)

	#show cards (one hidden)
	show_some(player_hand, dealer_hand)

	while playing:
		#prompt for Player to HIT or STAND
		hit_or_stand(deck, player_hand)

		#show cards (one hidden)
		show_some(player_hand, dealer_hand)

		#if player hand exceeds 21, run player_bust or break out of loop
		if player_hand.value > 21:
			player_busts(player_hand, dealer_hand, player_chips)
			break

		#if player hasn't busted, play dealer's hand until dealer reaches 17
		if player_hand.value <= 21:
			while dealer_hand.value < 17:
				hit(deck, dealer_hand)

			#show all cards
			show_all(player_hand, dealer_hand)

			#run different winning scenarios
			if dealer_hand.value > 21:
				dealer_busts(player_hand, dealer_hand, player_chips)
			elif dealer_hand.value > player_hand.value:
				dealer_wins(player_hand, dealer_hand, player_chips)
			elif dealer_hand.value < player_hand.value:
				player_wins(player_hand, dealer_hand, player_chips)
			else:
				push(player_hand, dealer_hand)

		#inform player of their chips total
		print('\n Player total chips are at: {}'.format(player_chips.total))

		#ask to play again
		new_game = input("Would you like to play another hand? y/n")

		if new_game[0].lower() == 'y':
			playing = True
			continue
		else:
			print('Thank you for playing! ')
			break
