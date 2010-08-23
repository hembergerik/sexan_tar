#!/usr/bin/python
from random import shuffle
from random import choice as random_choice

class RandomPlayer:
    def __init__(self):
        pass

    def select_card(self, piles, hand):
        return random_choice(hand)

    def select_pile(self, piles, hand):
        return random_choice(piles)

class RandomCheapPlayer(RandomPlayer):
    def select_pile(self, piles, hand):
        cheapest = min(len(pile) for pile in piles)
        all_cheap = [pile for pile in piles if len(pile) == cheapest]
        return random_choice(all_cheap)

class SortedPlayer(RandomPlayer):
    def select_card(self, piles, hand):
        hand_list = list(hand)
        hand_list.sort()
        return hand_list[0]

class ReverseSortedPlayer(RandomPlayer):
    def select_card(self, piles, hand):
        hand_list = list(hand)
        hand_list.sort()
        hand_list.reverse()
        return hand_list[0]

#102 cards
#cost of card TODO correct?
#card mod 5 == 0 => +1
#card mod 10 == 0 => +1
#card mod 11 == 0 => +4
class Card:
    def __init__(self, value):
        self.value = value
        self.cost = 1
        if self.value % 5 == 0:
            self.cost = self.cost + 1
        if self.value % 10 == 0:
            self.cost = self.cost + 1
        if self.value % 11 == 0:
            self.cost = self.cost + 4

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return ("Card value:%d cost:%d"%(self.value, self.cost))

def deal(deck, n):
    cards = deck[:n]
    del deck[:n]
    return cards

def get_random_start(player_count, deck_size, pile_count, hand_size):
    deck = [Card(i) for i in range(1, deck_size+1)]
    shuffle(deck)
    piles = tuple([c] for c in deal(deck, 4))
    hands = [sorted(deal(deck, hand_size)) for _ in xrange(player_count)]
    return piles, hands

def pick_card(player, piles, hand):
    selected_card = player.select_card(piles, tuple(hand))
    try:
        hand.remove(selected_card)
        return selected_card
    except:
        print 'Illegal choice'
        raise 

def pick_pile(player, piles, hand):
    static_piles = tuple(tuple(cards) for cards in piles)
    selected_pile = player.select_pile(static_piles, tuple(hand))
    pile_number = list(static_piles).index(selected_pile)
    return piles[pile_number]

def resolve_card_placement(piles, card, hand, penalty_pile, player, pile_size):
    distances = tuple(max(0, card.value - pile[-1].value) for pile in piles)
    lower_piles = tuple((pile[-1], pile) for pile in piles if pile[-1].value < card.value)
    if len(lower_piles) == 0:
        pile = pick_pile(player, piles, hand)
        take_pile = True
    else:
        _, pile = max(lower_piles)
        take_pile = len(pile) == pile_size
        #if take_pile: print "Sexan tar!!!!!!!",[str(card) for card in pile]
    if take_pile:
        penalty_pile.extend(pile)
        del pile[:]
    pile.append(card)
    #print card, piles

def do_turn(players, piles, hands, penalty_piles, pile_size):
    static_piles = tuple(tuple(cards) for cards in piles)
    selected_cards = tuple(pick_card(player, static_piles, hand) 
                           for player, hand in zip(players, hands))
    #print selected_cards
    placements = sorted(zip(selected_cards, hands, penalty_piles, players))
    for card, hand, penalty_pile, player in placements:
        resolve_card_placement(piles, card, hand, penalty_pile, player, pile_size)

def main():
    DECK_SIZE = 104
    PLAYERS = 4
    PILE_COUNT = 4
    PILE_SIZE = 5
    HAND_SIZE = 10
    ROUNDS = 1000
    total_scores = [0 for _ in xrange(PLAYERS)]
    total_total_scores = [0 for _ in xrange(PLAYERS)]
    game_wins = [0 for _ in xrange(PLAYERS)]
    for round in xrange(ROUNDS):
        scores = play_round(DECK_SIZE, PLAYERS, PILE_SIZE, PILE_COUNT, HAND_SIZE)
        total_scores = [t+s for t, s in zip(total_scores, scores)]        
        total_total_scores = [t+s for t, s in zip(total_total_scores, total_scores)]        
        if max(total_scores) >= 66:
            min_score = min(total_scores)
            for i in range(len(scores)):
                if total_scores[i] == min_score:
                    game_wins[i] = game_wins[i] + 1                    
                    total_scores = [0 for _ in xrange(PLAYERS)]
    print "Wins:",game_wins
    print "Total score sum:",total_total_scores

def play_round(DECK_SIZE, PLAYERS, PILE_SIZE, PILE_COUNT, HAND_SIZE):
    piles, hands = get_random_start(PLAYERS, DECK_SIZE, PILE_COUNT, HAND_SIZE)
    players = [RandomPlayer() for _ in xrange(PLAYERS)]
    players[0] = RandomCheapPlayer()
    players[1] = SortedPlayer()
    players[2] = ReverseSortedPlayer()
    penalty_piles = [[] for _ in xrange(PLAYERS)]
    
    def show():
        return
        print piles
        print hands
        print penalty_piles
        print

    show()
    for turn in xrange(HAND_SIZE):
        do_turn(players, piles, hands, penalty_piles, PILE_SIZE)
        show()
    return [sum([card.cost for card in pile]) for pile in penalty_piles]

if __name__ == '__main__':
    main()
