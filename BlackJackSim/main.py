#!/usr/bin/env python3
import random

from constants import SUITS, VALUES


class CardIdentifier(object):

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    # displays results with correct naming
    def __repr__(self):
        return repr(self.suit and self.value)


class Deck(object):

    def __init__(self):
        self.cards = self.build_deck()

    def build_deck(self):
        deck = []

        for suit in SUITS:
            for value in VALUES:
                deck.append(CardIdentifier(suit, value))

        return deck


class Dealer(Deck):
    dealer_hand = []
    bust = False


class Player(Deck):
    player_hand = []
    split_hand = []
    bust = False

    # TODO would like to properly implement a use for this
    def __init__(self):
        self.chip_amount = 250

        super(Player, self).__init__()


def find_value(cards):
    total = 0
    ace_present = False
    ace_total_deduction = 0

    for i in cards:
        if i.value == 'A':
            ace_present = True
            total += 11
        elif i.value in ['J', 'Q', 'K']:
            total += 10
        else:
            total += int(i.value)

        if ace_present and total > 21:
            if ace_total_deduction == 0:
                ace_total_deduction += 1
                total -= 10

    return total


class Round:
    """
    class for the round of blackjack controlling the flow of the game
    """
    def __init__(self):

        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.player_total = 0
        self.dealer_total = 0
        self.final_player_score = self.player_total
        self.final_dealer_score = self.dealer_total
        self.score_board = {}
        self.deal_cards()
        self.round_calculations()
        self.final_score()
        self.reset()

    def update_hand_value(self, is_dealer=False):
        """
        function for keeping player hand total updated
        for use as a helper function to users and logic regarding total value
        """

        if is_dealer:
            self.dealer_total = find_value(self.dealer.dealer_hand)

            return self.dealer_total

        else:
            self.player_total = find_value(self.player.player_hand)

            return self.player_total

    def check_bust(self, is_dealer=False):
        """
        function for checking whether player or dealer is bust
        :param is_dealer:
        :return:
        """
        if is_dealer and self.dealer_total > 21:
            self.dealer.bust = True
            return True

        elif self.player_total > 21:
            self.player.bust = True
            return self.player.bust

    def draw_cards(self, initial_draw=False, is_dealer=False):
        """
        function to draw cards, added initial_draw to be passed to determine whether 1 or 2 cards are needed
        :param initial_draw:
        :param is_dealer:
        :return:
        """

        if is_dealer is False:
            if initial_draw:

                for i in range(0, 2):
                    card_dealt = random.choice(self.deck.cards)
                    self.player.player_hand.append(card_dealt)
                    self.deck.cards.remove(card_dealt)

                return self.player.player_hand
            else:

                card_dealt = random.choice(self.deck.cards)
                self.player.player_hand.append(card_dealt)
                self.deck.cards.remove(card_dealt)

                return self.player.player_hand

        else:

            card_dealt = random.choice(self.deck.cards)
            self.dealer.dealer_hand.append(card_dealt)
            self.deck.cards.remove(card_dealt)

            return self.dealer.dealer_hand

    def deal_cards(self):
        """
        I added the dealer and player totals and hand clears as precaution as during testing it wasn't always resetting
        :return:
        """
        self.dealer_total = 0
        self.player_total = 0
        self.player.player_hand.clear()
        self.dealer.dealer_hand.clear()
        self.draw_cards(initial_draw=True, is_dealer=False)
        self.update_hand_value()
        self.draw_cards(initial_draw=True, is_dealer=True)
        self.update_hand_value(is_dealer=True)
        # self.dealer_draw_one = self.draw_cards()

        print("Player currently holds {} of {} and {} or {}".format(self.player.player_hand[0].value,
                                                                    self.player.player_hand[0].suit,
                                                                    self.player.player_hand[1].value,
                                                                    self.player.player_hand[1].suit
                                                                    ))

        # TODO come back to this and implement option for splitting if there is a pair in player hand
        print("Dealer has drew a {} of {}".format(self.dealer.dealer_hand[0].value,
                                                  self.dealer.dealer_hand[0].suit))
        player_action = input("Do you want to Hit or Stick?: [h/s]").lower()
        if player_action.lower() == 'h':
            # self.player.player_hand += self.player.get_cards(1) OLD WAY of drawing cards for reference
            self.draw_cards(is_dealer=False)
            self.update_hand_value()
            print(
                "Player has drew a {} of {}".format(self.player.player_hand[2].value, self.player.player_hand[2].suit))
            self.check_bust(is_dealer=False)
            if self.player.bust is False:
                player_action_two = input(
                    "You currently hold {} would you like to Hit or Stick? [h/s]".format(self.player_total))
                if player_action_two == 'h':
                    self.draw_cards(is_dealer=False)
                    self.update_hand_value()
                    print(
                        "Player has drew a {} of {}".format(self.player.player_hand[3].value,
                                                            self.player.player_hand[3].suit))
                    self.check_bust()
                    if self.player.bust is False:
                        player_action_three = input(
                            "Player Hand: {} and Total Value: {} would you like to Hit or Stick? [h/s]".format(
                                self.player.player_hand, self.player_total))
                        if player_action_three == 'h':
                            self.draw_cards(is_dealer=False)
                            self.update_hand_value()
                            print(
                                "Player has drew a {} of {}".format(self.player.player_hand[4].value,
                                                                    self.player.player_hand[4].suit))
                            self.check_bust()
                            if self.player.bust is False:
                                player_action_four = input(
                                    "You currently hold {} would you like to Hit or Stick? [h/s]".format(
                                        self.player_total))

            return self.player_total
        elif player_action.lower() == 's':
            self.draw_cards(is_dealer=True)
            self.dealer_total = find_value(self.dealer.dealer_hand)
            return self.dealer_total
        else:
            print("Please Enter one of the stated choices")

    def round_calculations(self):

        print(
            "Hold While we begin Calculations.....")  # This was mainly for testing to help me keep track of where i was

        self.check_bust(is_dealer=False)

        if self.player_total < 22:
            self.draw_cards(is_dealer=True)
            self.update_hand_value(is_dealer=True)
            print(
                "Dealer has drew a {} of {}".format(self.dealer.dealer_hand[1].value, self.dealer.dealer_hand[1].suit))
            print("Dealer Total is {}".format(self.dealer_total))
            self.final_player_score = self.player_total

        self.check_bust(is_dealer=True)
        # Set to 22 instead of 21 as during final testing i got one hit 21 for dealer and it marked as bust
        if self.dealer_total < 22:
            self.final_dealer_score = self.dealer_total

    def final_score(self):
        self.score_board = {'dealer': 0, 'player': 0}
        if self.player.bust:
            print("Player is Busted")
            self.score_board['dealer'] += 1

        elif self.dealer.bust:
            print("Dealer is Busted")
            self.score_board['player'] += 1
        elif self.final_player_score > self.final_dealer_score:
            print("Player has Won")
            self.score_board['player'] += 1
        elif self.final_dealer_score > self.final_player_score:
            print("Dealer has Won")
            self.score_board['dealer'] += 1
        else:
            print("It seems you both scored the same, play again ")

        return self.score_board

    def reset(self):
        self.dealer_total = 0
        self.player_total = 0
        self.player.player_hand.clear()
        self.dealer.dealer_hand.clear()


class Game:

    def __init__(self):
        # Asks player if they would to begin
        game_start = input("Would you like to play a game?: [yes/no]").lower()

        if game_start.lower() == 'yes':
            Round()
            while True:
                game_restart = input("Would you like to play again: [yes/no]").lower()
                if game_restart.lower() == 'yes':
                    Round()

        else:
            warning = input("Are you sure you don't want to play [yes/no]").lower()
            if warning.lower() == 'yes':
                exit()


if __name__ == '__main__':
    game = Game()
