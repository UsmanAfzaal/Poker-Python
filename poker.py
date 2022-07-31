import time
from random import shuffle
import random

# The Self-Taught Programmer The Definitive Guide to Programming Professionally (Cory Althoff)

class Card:
    suits = ["clubs", "diamonds", "hearts", "spades"]
    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, value, suit):
        """suit and value should be integer"""
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        if self.value < other.value:
            return True
        if self.value == other.value:
            if self.suit < other.suit:
                return True
        else:
            return False
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        if self.value == other.value:
            if self.suit > other.suit:
                return True
        else:
            return False
        return False

    def __repr__(self):
        return self.values[self.value] + " of " + self.suits[self.suit]


class Deck:
    def __init__(self):
        self.cards = []

        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))

        shuffle(self.cards)

    def make_hand(self):
        hand_list = []
        if len(self.cards) == 1:
            return
        for i in range(5):
            pop = random.choice(self.cards)
            self.cards.remove(pop)
            hand_list.append(pop)
        return hand_list


class Player:
    def __init__(self, name):
        self.wins = 0
        self.hand = []  # List/combination of 5 cards
        self.name = name

    def print_hand(self):
        func = lambda x: x.values[x.value] + ' of ' + x.suits[x.suit]
        playerhand = [func(self.hand[index]) for index in range(len(self.hand))]
        print("{}'s hand contains {}".format(self.name, playerhand))


class Poker:
    def __init__(self):
        name1 = input("Enter name of player 1: ")
        name2 = input("Enter name of player 2: ")

        # making deck
        self.deck = Deck()

        self.player1 = Player(name1)
        self.player2 = Player(name2)

    # https://github.com/annaymj/Python-Code/blob/master/Poker.py

    def royal_flush(self, cardlist: list, player):  # change card_list to hand if needed
        rank = 10
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        current_suit = sorted_cardlist[0].suit
        current_value = sorted_cardlist[0].value

        for card in sorted_cardlist:
            if card.value != current_value or card.suit != current_suit:
                flag = False
                break
            else:
                current_value -= 1

        if sorted_cardlist[0] == 14 and flag == True:
            print("{} has a Royal Flush".format(player))
            return rank
        else:
            return self.straight_flush(cardlist, player)

    def straight_flush(self, cardlist, player):
        rank = 9
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        current_suit = sorted_cardlist[0].suit
        current_value = sorted_cardlist[0].value

        for card in sorted_cardlist:
            if card.value != current_value or card.suit != current_suit:
                flag = False
                break
            else:
                current_value -= 1

        if flag:
            print("{} has a Straight Flush".format(player))
            return rank
        else:
            return self.four_of_kind(cardlist, player)

    def four_of_kind(self, cardlist, player):
        rank = 8
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        sorted_valuelist = [sorted_cardlist[i].value for i in range(len(sorted_cardlist))]

        most_repeated_val = max(sorted_valuelist, key=sorted_valuelist.count)
        count_most_rep = sorted_valuelist.count(most_repeated_val)

        if count_most_rep != 4:
            flag = False

        if flag:
            print("{} has a Four of a Kind".format(player))
            return rank
        else:
            return self.full_house(cardlist, player)

    def full_house(self, cardlist, player):
        rank = 7
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        sorted_valuelist = [sorted_cardlist[i].value for i in range(len(sorted_cardlist))]

        most_repeated_val = max(sorted_valuelist, key=sorted_valuelist.count)
        count_most_rep = sorted_valuelist.count(most_repeated_val)

        least_repeated_val = min(sorted_valuelist, key=sorted_valuelist.count)
        count_least_rep = sorted_valuelist.count(least_repeated_val)

        if count_least_rep != 2 or count_most_rep != 3:
            flag = False
        else:
            flag = True

        if flag:
            print("{} has a Full House".format(player))
            return rank
        else:
            return self.flush(cardlist, player)

    def flush(self, cardlist, player):
        rank = 6
        flag = True

        card_suit_list = [cardlist[i].suit for i in range(len(cardlist))]
        most_repeated_suit = max(card_suit_list, key=card_suit_list.count)
        count_most_repeated_suit = card_suit_list.count(most_repeated_suit)

        if count_most_repeated_suit != 5:
            flag = False

        if flag:
            print("{} has a Flush".format(player))
            return rank
        else:
            return self.straight(cardlist, player)

    def straight(self, cardlist, player):
        rank = 5
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        current_value = sorted_cardlist[0].value

        for card in sorted_cardlist:
            if card.value == current_value:
                current_value -= 1
            else:
                flag = False
                break

        if flag:
            print("{} has a Straight".format(player))
            return rank
        else:
            return self.three_of_kind(cardlist, player)

    def three_of_kind(self, cardlist, player):
        rank = 4
        flag = True
        sorted_cardlist = sorted(cardlist, key=lambda x: x.value, reverse=True)
        sorted_valuelist = [sorted_cardlist[i].value for i in range(len(sorted_cardlist))]

        most_repeated_val = max(sorted_valuelist, key=sorted_valuelist.count)
        count_most_rep = sorted_valuelist.count(most_repeated_val)

        if count_most_rep != 3:
            flag = False

        if flag:
            print("{} has a Three of a Kind".format(player))
            return rank
        else:
            return self.two_pair(cardlist, player)

    def two_pair(self, cardlist, player):
        rank = 3
        flag = True

        value_list = [cardlist[i].value for i in range(len(cardlist))]
        # set would ensure that we are only counting for each instance once
        value_set_list = list(set(value_list))

        # checking how many instances of each value is present in the original list
        number_of_instances = []
        for i in range(len(value_set_list)):
            inst = value_list.count(value_set_list[i])
            number_of_instances.append(inst)

        # checking if there are two "2's" to verify the presence of two pairs
        if number_of_instances.count(2) != 2:
            flag = False

        if flag:
            print("{} has a Two Pair".format(player))
            return rank
        else:
            return self.pair(cardlist, player)

    def pair(self, cardlist, player):
        rank = 2
        flag = True
        value_list = [cardlist[i].value for i in range(len(cardlist))]
        value_set_list = list(set(value_list))

        number_of_instances = []
        for i in range(len(value_set_list)):
            inst = value_list.count(value_set_list[i])
            number_of_instances.append(inst)

        if number_of_instances.count(2) != 1:
            flag = False

        if flag:
            print("{} has a Pair".format(player))
            return rank
        else:
            return self.high_card()

    def high_card(self):
        rank = 1
        flag = True

        return rank

    def winner(self, player1, player2):
        if player1.wins > player2.wins:
            return f"{player1.name} is the winner"
        if player2.wins > player1.wins:
            return f"{player2.name} is the winner"
        return "It is a Draw"

    def game(self):
        # can also use 'cards: list' variable also below in the len() function, since both points to same list
        cards = self.deck.cards
        print("starting game!")

        response = None
        while len(self.deck.cards) >= 10 and response != 'q':
            response = input("Press 'q' to quit, any other key to continue\n")

            self.player1.hand = self.deck.make_hand()
            self.player2.hand = self.deck.make_hand()

            self.player1.print_hand()
            self.player2.print_hand()

            print("Comparing the hands of both players")
            time.sleep(1)

            # determining the hand of each player
            player1_rank = self.royal_flush(self.player1.hand, self.player1.name)
            player2_rank = self.royal_flush(self.player2.hand, self.player2.name)

            if player1_rank == player2_rank:
                if player1_rank == 1:
                    value_list_player1 = [self.player1.hand[i].value for i in range(len(self.player1.hand))]
                    max_value_player1 = max(value_list_player1)
                    extracted_card_player1 = self.player1.hand[value_list_player1.index(max_value_player1)]

                    value_list_player2 = [self.player2.hand[i].value for i in range(len(self.player2.hand))]
                    max_value_player2 = max(value_list_player2)
                    extracted_card_player2 = self.player2.hand[value_list_player2.index(max_value_player2)]

                    if extracted_card_player1 > extracted_card_player2:
                        print("{} has high card which is {}".format(self.player1.name, extracted_card_player1))
                        print("{} wins this round".format(self.player1.name))
                        self.player1.wins += 1
                    else:
                        print("{} has high card which is {}".format(self.player2.name, extracted_card_player2))
                        print("{} wins this round".format(self.player2.name))
                        self.player2.wins += 1

                print("This round is a draw")
            else:
                if player1_rank > player2_rank:
                    print("{} wins this round".format(self.player1.name))
                    self.player1.wins += 1
                if player2_rank > player1_rank:
                    print("{} wins this round".format(self.player2.name))
                    self.player2.wins += 1

            # if len(self.deck) == 1 or response == 'q' # use if you want to put this block inside the while loop

        return print("The game has ended. {}".format(self.winner(self.player1, self.player2)))


if __name__ == "__main__":
    # Start the game
    poker = Poker()
    poker.game()
