import random
from collections import deque

#Constant variables

FACES = { 9:'J', 10:'Q', 11:'K', 12:'A' }

# Values 0-12 will represent cards 2-Ace
def shuffle_deck():
    deck = []
    for i in range(52):
        deck.insert(int(random.random() * len(deck)), i % 13)
    return deck


def is_valid_card(val):
    if val not in range(13):
        raise Exception('val must be from 0 to 12')


def to_symbol(card):
    is_valid_card(card)
    if card >= 9:
        return FACES[card]
    return card + 2


def to_symbols(cards):
    return [to_symbol(c) for c in cards]


def check_deck(deck):
    # array of 13 0's, used to track number of each card type
    num_cards = [0 for _ in range(13)]
    for card in deck:
        is_valid_card(card)
        num_cards[card] += 1
    dict = {to_symbol(n): num_cards[n] for n in range(13)}
    for val in dict.values():
        if val != 4:
            raise Exception('incorrect number of cards in deck!')
    print(dict)


def deal_hands(deck):
    hands = [deque([]), deque([])]
    for index, card in enumerate(deck):
        hands[index % 2].append(card)
    return hands


def play_war():
    deck = shuffle_deck()
    print(f'deck: {to_symbols(deck)}')
    # return
    hands = deal_hands(deck)
    print(f'Player 1: {to_symbols(hands[0])}\nPlayer 2: {to_symbols(hands[1])}')
    print(f'Player 1 val: {sum(hands[0])}\nPlayer 2 val: {sum(hands[1])}')
    ini_vals = [sum(hands[0]), sum(hands[1])]

    play = [-1, -1]
    pot = []
    rounds = 0
    wars = 0
    while len(hands[0]) > 0 and len(hands[1]) > 0:
        while play[0] == play[1]:
            # if this isn't the first cards down (aka, it's a WAR) send extra cards to pot
            if play[0] > 0:
                if len(hands[0]) == 0 or len(hands[1]) == 0:
                    break;
                if random.random() < 0.5:
                    pot.extend([hands[0].popleft(), hands[1].popleft()])
                else:
                    pot.extend([hands[1].popleft(), hands[0].popleft()])
                wars += 1
            # take 1 card from each player's hand
            if len(hands[0]) == 0 or len(hands[1]) == 0:
                break;
            play[0] = hands[0].popleft()
            play[1] = hands[1].popleft()
            # these cards go into the winning pot, AT RANDOM because if p1's card goes first loops are common!
            if random.random() < 0.5:
                pot.extend([play[0], play[1]])
            else:
                pot.extend([play[1], play[0]])
            print(f'{to_symbol(play[0])} vs {to_symbol(play[1])}, pot: {to_symbols(pot)}')
        else:
            if play[0] > play[1]:
                hands[0].extend(pot)
                print('Player 1s pot')
            else:
                hands[1].extend(pot)
                print('Player 2s pot')
            print(f'Player 1: {to_symbols(hands[0])}\nPlayer 2: {to_symbols(hands[1])}')
            # print(deck)
            play = [-1, -1]
            pot = []
            rounds += 1
    else:
        if len(hands[0]) == 0:
            print('Player 2 Wins!')
        else:
            print('Player 1 Wins!')
        print(f'This game lasted {rounds} rounds and had {wars} wars.')
        print(f'Player 1 initial val: {ini_vals[0]}\nPlayer 2 initial val: {ini_vals[1]}')


