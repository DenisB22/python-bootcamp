import random


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Please enter your bet (integer number): "))
            if chips.bet > chips.total:
                print("You do not have enough chips to do this bet. Try again.")
            else:
                break
        except ValueError:
            print("You entered wrong type value. Please try again...")


def hit(deck, hand):
    # When you go for hitting, you are dealt one additional card
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        player_choice = input("Please choose an option - Hit or Stand: \n")

        if player_choice.lower() == "hit":
            hit(deck, hand)
        elif player_choice.lower() == "stand":
            # If you choose to stand, you are keeping the cards you have
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print("Sorry, I did not understand that, Please enter Hit or Stand only!")
            continue
        break


def show_some(player, dealer):
    dealer_cards = [f'{x.suit} of {x.rank}' for x in dealer.cards[1:]]
    player_cards = [f'{x.suit} of {x.rank}' for x in player.cards]

    print(f"The dealer cards are, where the first is hidden: {', '.join(dealer_cards)}")
    print(f"The player cards are: {', '.join(player_cards)}")


def show_all(player, dealer):
    dealer_cards = [f'{x.suit} of {x.rank}' for x in dealer.cards]
    player_cards = [f'{x.suit} of {x.rank}' for x in player.cards]

    print(f"The dealer cards are: {', '.join(dealer_cards)}")
    print(f"The value of the dealer cards is: {dealer.value}")
    print(f"The player cards are: {', '.join(player_cards)}")
    print(f"The value of the player cards is: {player.value}")


def player_busts(player_hand, dealer_hand, chips):
    # Losing hand, dead hand, or the bust
    # Each hand that is one points short compared to the dealer's score
    # Every hand with total sum of 22 or higher
    print("BUST PLAYER")
    chips.lose_bet()


def player_wins(player_hand, dealer_hand, chips):
    # 2-card hand that totals 21 points
    # higher score than the dealer's
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_busts(player_hand, dealer_hand, chips):
    print("PLAYER WINS! DEALER BUSTED! ")
    chips.win_bet()


def dealer_wins(player_hand, dealer_hand, chips):
    print("DEALER WINS!")
    chips.lose_bet()


def push(player_hand, dealer_hand):
    # if the dealer holds 21, the result is so-called Push, meaning that
    # the initial bet is returned to you and you neither win nor loose
    print("Dealer and player tie! PUSH")


suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")

values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit} of {self.rank}"


class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.all_cards.append(card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal(self):
        return self.all_cards.pop()

    def __str__(self):
        deck_comp = ''
        for card in self.all_cards:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        # card passed in
        # from Deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THEN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


while True:
    # Print an opening statement
    print("Welcome to the Blackjack game.")

    # Create & Shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            # card = deck.deal()
            # dealer_hand.add_card(card)
            # print(dealer_hand.cards)
            # print(dealer_hand.value)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
            break

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    print(f"You have: {player_chips.total} total chips")

    continue_playing = input("Do you want to continue playing? - Y/N\n")

    if continue_playing[0].lower() == 'y':
        continue
    elif continue_playing[0].lower() == 'n':
        print("Thank you for playing")
        break



