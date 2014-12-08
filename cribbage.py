#!/usr/bin/env python
"""
A module containing a collection of methods for scoring a cribbage hand.

"""
import itertools

from card import Suit, Rank, Deck


def score_hand(hand, starter, verbose=False):
    """
    Score the hand.

    :param hand: a four card hand
    :param starter: the starter card
    :param verbose: flag for printing
    :return: the score of the hand


    """
    pts = 0

    p_15 = score_15(hand, starter)
    pts += p_15
    if verbose:
        print "  15s:   {:>2}".format(p_15)

    p_pair = score_pairs(hand, starter)
    pts += p_pair
    if verbose:
        print "  pairs: {:>2}".format(p_pair)

    p_run = score_runs(hand, starter)
    pts += p_run
    if verbose:
        print "  runs:  {:>2}".format(p_run)

    p_flush = score_flush(hand, starter)
    pts += p_flush
    if verbose:
        print "  flush: {:>2}".format(p_flush)

    p_nibs = score_nibs(hand, starter)
    pts += p_nibs
    if verbose:
        print "  nibs:  {:>2}".format(p_nibs)

    return pts


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

    5 in a row: A 2 3 4 5   this is a run of 5
                0 1 1 1 1

    4 in a row: A 2 3 4 6   this has one run of 4

                A 2 3 4    A 2 3 6    A 2 4 6   A 3 4 6   2 3 4 6
                0 1 1 1    0 1 1 3    0 1 2 2   0 3 1 2   0 1 1 2

    3 in a row: A 2 3 3 6   this has two runs of 3

                A 2 3   A 2 3   A 2 6   A 3 3   A 3 6   A 3 6   2 3 3   2 3 6   2 3 6   3 3 6
                0 1 1   0 1 1   0 1 4   0 2 0   0 2 3   0 4 1   0 1 0   0 1 3   0 1 3   0 0 3

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

    # first check for a run of 5
    scards = sorted(cards)

    ds = []
    c0 = scards[0]
    for c in scards:
        d = c.del_rank(c0)
        ds.append(d)
        c0 = c
#        print c, c0, d

    # if this matches, we have a run of 5 and can return
    if ds == [0, 1, 1, 1, 1]:
        return 5

    # now check for runs of 4
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

        # if this matches, we have a run of 4
        if ds == [0, 1, 1, 1]:
            p += 4
    # if p is no longer 0, we found runs of 4 and can return
    if p > 0:
        return p

    # finally check for runs of 3
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

        # if this matches, we have a run of 3
        if ds == [0, 1, 1]:
            p += 3

    # here we have runs of 3, or nothing
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
    verbose = False
    deck = Deck()
    n_hands = 100000

    total = 0
    mx = -1
    for h in range(n_hands):
        deck.shuffle()

        hand = []
        for i in range(4):
            hand.append(deck.deal.next())
        starter = deck.deal.next()

        if verbose:
            print "Hand {}: [{}] {} {} {} {}".format(h, starter, *hand)

        pts = score_hand(hand, starter, verbose)

        if verbose:
            print "  Total: {:>2}".format(pts)

        if pts > mx:
            mx = pts

        total += pts

    avg = float(total)/n_hands
    print "Avg = %f   Max = %d" % (avg, mx)
