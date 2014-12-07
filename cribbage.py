#!/usr/bin/env python
import math
import itertools

from card import Suit, Rank, Card, Deck


def score_hand(hand, starter):
    """

    :param hand:
    :param starter:
    """
    points = 0

    print "Checking for 15s..."
    points += score_15(hand, starter)
    print "  Points = %d" % points

    print "Checking for pairs..."
    points += score_pairs(hand, starter)
    print "  Points = %d" % points

    print "Checking for runs..."
    points += score_runs(hand, starter)
    print "  Points = %d" % points

    print "Checking for flush..."
    points += score_flush(hand, starter)
    print "  Points = %d" % points

    print "Checking for right jack..."
    points += score_nibs(hand, starter)
    print "  Points = %d" % points


def score_15(hand, starter):
    """
    Score hand for 15s.

    :param hand: list of cards in hand
    :param starter: the starter card
    :return: the number of points from 15's

    >>> from card import Card
    >>> hand = [Card(Rank.jack, Suit.hearts), \
                Card(Rank.ace,  Suit.spades), \
                Card(Rank.two,  Suit.clubs),  \
                Card(Rank.ace,  Suit.diamonds)]
    >>> starter = Card(Rank.five, Suit.hearts)
    >>> score_15(hand, starter)
    2

    """
    # combine hand and starter
    cards = hand[:]
    cards.append(starter)

    count = 0
    # iterate over all combinations of 2, 3, 4, and 5 cards
    for l in range(2,6):
        for cs in itertools.combinations(cards, l):
            s = 0
            # sum up the values of this combination
            for c in cs:
                s += c.get_value()
            if s == 15:
                # we have a 15
#                print "   ", cs
                count += 1

    # 2 points for each 15
    return 2*count


def score_pairs(hand, starter):
    """
    Score hand for pairs.

    :param hand: list of cards in hand
    :param starter: the starter card
    :return: the number of points from pairs

    Note that 3-of-a-kind is just 3 pairs (6 pts) and a 4-of-a-kind is 6 pairs (12 pts).

    >>> from card import Card
    >>> hand = [Card(Rank.jack, Suit.hearts), \
                Card(Rank.ace,  Suit.spades), \
                Card(Rank.two,  Suit.clubs),  \
                Card(Rank.ace,  Suit.diamonds)]
    >>> starter = Card(Rank.five, Suit.hearts)
    >>> score_pairs(hand, starter)
    2

    """
    # combine hand and starter
    cards = hand[:]
    cards.append(starter)

    count = 0
    # iterate over all combinations of 2 cards
    for cs in itertools.combinations(cards, 2):
        if cs[0].rank == cs[1].rank:
            # we have a pair
#            print cs
            count += 1

    # 2 points for each pair
    return 2*count


def score_runs(hand, starter):
    """
    Score hand for runs.

    :param hand: list of cards in hand
    :param starter: the starter card
    :return: the number of points from runs

    5 in a row:
    A 2 3 4 5
    0 1 1 1 1

    4 in a row: A 2 3 4 6

                A 2 3 4    A 2 3 6    A 2 4 6   A 3 4 6   2 3 4 6
                0 1 1 1    0 1 1 3    0 1 2 2   0 3 1 2   0 1 1 2

    3 in a row:
    6 5 3 2 A    6 5 4 2 A    7 5 4 3 A
      1 2 1 1      1 1 2 1      2 1 1 2

    >>> from card import Card
    >>> hand = [Card(Rank.jack, Suit.hearts), \
                Card(Rank.ten,  Suit.spades), \
                Card(Rank.nine,  Suit.clubs),  \
                Card(Rank.queen,  Suit.diamonds)]
    >>> starter = Card(Rank.king, Suit.hearts)
    >>> score_runs(hand, starter)
    5
    >>> starter = Card(Rank.queen, Suit.hearts)
    >>> score_runs(hand, starter)
    8
    >>> starter = Card(Rank.two, Suit.hearts)
    >>> score_runs(hand, starter)
    4

    """
    # combine hand and starter
    cards = hand[:]
    cards.append(starter)

    scards = sorted(cards)
#    print scards

    ds = []
    c0 = scards[0]
    for c in scards:
        d = c.del_rank(c0)
        ds.append(d)
        c0 = c
#        print c, c0, d

    if ds == [0, 1, 1, 1, 1]:
        return 5

    p = 0
    for cs in itertools.combinations(cards, 4):
        scards = sorted(cs)
#        print scards
        ds = []
        c0 = scards[0]

        for c in scards:
            d = c.del_rank(c0)
            ds.append(d)
            c0 = c
#            print c, c0, d

        if ds == [0, 1, 1, 1]:
            p += 4
    if p > 0:
        return p

    p = 0
    for cs in itertools.combinations(cards, 3):
        scards = sorted(cs)
#        print scards
        ds = []
        c0 = scards[0]

        for c in scards:
            d = c.del_rank(c0)
            ds.append(d)
            c0 = c
#            print c, c0, d

        if ds == [0, 1, 1]:
            p += 3

    return p


def score_flush(hand, starter):
    """
    Score hand for a flush.

    :param hand: list of cards in hand
    :param starter: the starter card
    :return: the number of points from a flush

    - check hand for 4
    - check starter for 5

    >>> from card import Card
    >>> hand = [Card(Rank.jack, Suit.hearts), \
                Card(Rank.ace,  Suit.hearts), \
                Card(Rank.two,  Suit.hearts),  \
                Card(Rank.four,  Suit.hearts)]
    >>> starter = Card(Rank.five, Suit.hearts)
    >>> score_flush(hand, starter)
    5
    >>> starter = Card(Rank.five, Suit.clubs)
    >>> score_flush(hand, starter)
    4
    """
    cards = hand[:]

    # if any pair of the 4 cards have different suits, there is no flush
    for cs in itertools.combinations(cards, 2):
        if cs[0].get_suit() != cs[1].get_suit():
            return 0

    # got at least 4, check the starter for 5
    if cards[0].get_suit() == starter.get_suit():
        return 5
    else:
        return 4


def score_nibs(hand, starter):
    """
    Check hand for his nibs.

    :param hand: list of cards in hand
    :param starter: the starter card
    :return: points for his nibs

    >>> from card import Card
    >>> hand = [Card(Rank.jack, Suit.hearts), \
                Card(Rank.ace,  Suit.spades), \
                Card(Rank.two,  Suit.clubs),  \
                Card(Rank.ace,  Suit.diamonds)]
    >>> starter = Card(Rank.five, Suit.hearts)
    >>> score_nibs(hand, starter)
    1
    >>> starter = Card(Rank.five, Suit.diamonds)
    >>> score_nibs(hand, starter)
    0

    """
    for c in hand:
        if c.rank.rank == Rank.jack:
            if c.suit == starter.suit:
                return 1
    return 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()

#   Play around
    deck = Deck()
    deck.shuffle()
    hand = []
    for i in range(4):
        hand.append(deck.deal.next())
    starter = deck.deal.next()

    print 'Hand: ',
    for c in hand:
        print c,
    print '[', starter, ']'

    score_hand(hand, starter)