#!/usr/bin/env python
"""
A module that defines some classes that model playing cards.

"""
import math
import random


class Suit(object):
    """
    A class representing the suit of a playing card.

    """

    spades, hearts, diamonds, clubs = 'Spades', 'Hearts', 'Diamonds', 'Clubs'
    suits = [spades, hearts, diamonds, clubs]

    def __init__(self, suit):
        """
        Create a suit object.

        >>> s = Suit(Suit.clubs)

        """
        assert(suit in self.suits)
        self.suit = suit

    def __eq__(self, other):
        """
        Provide a test of equality.

        :param other: an other Suit object
        :return: a boolean

        >>> s1 = Suit(Suit.hearts)
        >>> s2 = Suit(Suit.hearts)
        >>> s3 = Suit(Suit.spades)
        >>> s1 == s2
        True
        >>> s1 == s3
        False

        """
        return self.suit == other.suit

    def __str__(self):
        """
        Provide a short string representation.

        :return: a short string

        >>> str(Suit(Suit.diamonds))
        'D'

        """
        if self.suit == 'Spades':
            return 'S'
        elif self.suit == 'Hearts':
            return 'H'
        elif self.suit == 'Diamonds':
            return 'D'
        else:
            return 'C'

    def __unicode__(self):
        """
        Provide a unicode symbol for pretty printing.

        :return: a unicode string

        >>> unicode(Suit(Suit.diamonds))
        u'\u2666'

        """
        if self.suit == 'Spades':
            return u'\u2660'
        elif self.suit == 'Hearts':
            return u'\u2665'
        elif self.suit == 'Diamonds':
            return u'\u2666'
        else:
            return u'\u2663'

    def __repr__(self):
        """
        Provide a useful string representation.

        :return: a useful string representation

        >>> repr(Suit(Suit.diamonds))
        "Suit('Diamonds')"

        """
        return "{}('{}')".format(self.__class__.__name__, self.suit)


class Rank(object):
    """
    A class representing the rank of a playing card

    """
    ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king = \
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
    ranks = [ace, two, three, four, five, six, seven, eight, nine, ten, jack, queen, king]

    def __init__(self, rank):
        """
        Create a Rank object.

        :param rank: integer representation of the rank (1-13)

        >>> r = Rank(Rank.two)

        """
        assert(rank in self.ranks)
        self.rank = rank

    def __eq__(self, other):
        """
        Provide a test of equivalence.

        :param other: an other Rank object
        :return: a boolean

        >>> r1 = Rank(Rank.three)
        >>> r2 = Rank(Rank.three)
        >>> r3 = Rank(Rank.five)
        >>> r1 == r2
        True
        >>> r1 == r3
        False

        """
        return self.rank == other.rank

    def __lt__(self, other):
        """
        Provide a definition of ordering.

        :param other: an other Rank object
        :return: a boolean

        >>> r1 = Rank(Rank.three)
        >>> r2 = Rank(Rank.three)
        >>> r3 = Rank(Rank.five)
        >>> r1 < r2
        False
        >>> r1 < r3
        True

        """
        return self.rank < other.rank

    def __str__(self):
        """
        Provide a short string representation.

        :return: a short string

        >>> str(Rank(Rank.jack))
        'J'

        """
        if self.rank == 1:
            return 'A'
        elif self.rank == 11:
            return 'J'
        elif self.rank == 12:
            return 'Q'
        elif self.rank == 13:
            return 'K'
        else:
            return str(self.rank)

    def __unicode__(self):
        """
        Provide a unicode symbol for pretty printing.

        :return: a unicode string

        >>> unicode(Rank(Rank.jack))
        u'J'

        """
        return unicode(str(self))

    def __repr__(self):
        """
        Provide a useful string representation.

        :return: a useful string representation

        >>> repr(Rank(Rank.jack))
        'Rank(11)'

        """
        return "{}({})".format(self.__class__.__name__, self.rank)


class Card(object):
    """
    A class representing a playing card.

    """

    def __init__(self, rank, suit):
        """
        Create a card object.
        
        args:
            rank (int): the rank of the card (1-13)
            suit (string): the suit of the card

        >>> twoOfClubs = Card(Rank.two, Suit.clubs)
        >>> twoOfClubs.rank
        Rank(2)
        >>> twoOfClubs.suit
        Suit('Clubs')
        
        """
        self.rank = Rank(rank)
        self.suit = Suit(suit)

    def get_suit(self):
        """
        Get the suit of the card.

        :return: the suit

        >>> Card(Rank.jack, Suit.spades).get_suit()
        'Spades'

        """
        return self.suit.suit

    def get_rank(self):
        """
        Get the rank of the card.
        
        >>> Card(Rank.jack, Suit.spades).get_rank()
        11
        
        """
        return self.rank.rank

    def get_value(self):
        """

        >>> Card(Rank.jack, Suit.spades).get_value()
        10
        
        """
        if self.get_rank() > 10:
            return 10
        else:
            return self.get_rank()

    def __str__(self):
        """
        Get a string representation of the card.

        >>> str(Card(Rank.jack, Suit.spades))
        'JS'

        """
        return str(self.rank) + str(self.suit)

    def __unicode__(self):
        """
        Get a unicode representation of the card.

        >>> unicode(Card(Rank.jack, Suit.spades))
        u'J\u2660'

        """
        return unicode(self.rank) + unicode(self.suit)

    def __repr__(self):
        """
        Get a useful string representation.

        >>> repr(Card(Rank.jack, Suit.spades))
        "Card(11, 'Spades')"

        """
        return "{}({}, '{}')".format(self.__class__.__name__, self.get_rank(), self.get_suit())

    def __eq__(self, other):
        """
        Test of equality of two cards.

        :param other: another card object
        :return: a boolean

        >>> Card(Rank.king, Suit.spades) == Card(Rank.king, Suit.clubs)
        False
        >>> Card(Rank.king, Suit.spades) == Card(Rank.ace, Suit.spades)
        False
        >>> Card(Rank.king, Suit.spades) == Card(Rank.king, Suit.spades)
        True

        """
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        """
        Define ordering of cards.

        :param other: another card object
        :return: a boolean

        >>> Card(Rank.ace, Suit.spades) < Card(Rank.ace, Suit.clubs)
        False
        >>> Card(Rank.ace, Suit.spades) < Card(Rank.ten, Suit.clubs)
        True

        """
        return self.rank < other.rank

    def same_suit(self, other):
        """
        Check if two cards have the same suit.

        >>> Card(Rank.jack, Suit.spades).same_suit(Card(Rank.ten, Suit.spades))
        True
        >>> Card(Rank.jack, Suit.spades).same_suit(Card(Rank.jack, Suit.hearts))
        False

        """
        return self.suit == other.suit

    def same_rank(self, other):
        """
        Check if two cards have the same rank.

        >>> Card(Rank.jack, Suit.spades).same_rank(Card(Rank.ten, Suit.spades))
        False
        >>> Card(Rank.jack, Suit.spades).same_rank(Card(Rank.jack, Suit.hearts))
        True

        """
        return self.rank == other.rank

    def del_rank(self, other):
        """
        Return the number of ranks separating this card from another.

        >>> Card(Rank.jack, Suit.spades).del_rank(Card(Rank.ten, Suit.spades))
        1
        >>> Card(Rank.jack, Suit.spades).del_rank(Card(Rank.jack, Suit.hearts))
        0

        """
        return int(math.fabs(self.get_rank() - other.get_rank()))


class Deck(object):
    """
    A class representing a deck of playing cards.

    """

    def __init__(self, rng=None):
        """
        Create a deck (and shuffle it).

        :param rng: an optional random number generator

        >>> deck = Deck()

        """
        self.cards = []

        # Loop over suits
        for s in Suit.suits:

            # Loop over ranks
            for r in Rank.ranks:
                self.cards.append(Card(r, s))

        self.rng = rng or random.Random()
        self.deal = self.cards.__iter__()
        self.shuffle()

    def get_cards(self):
        """
        Get the list of cards.

        >>> deck = Deck()
        >>> len(deck.get_cards())
        52

        """
        return self.cards

    def shuffle(self):
        """
        Shuffle the deck.

        >>> deck = Deck()
        >>> deck.shuffle()
        >>> len(deck.cards)
        52

        """

        self.rng.shuffle(self.cards)
        # get a new iterator
        self.deal = self.cards.__iter__()

    def __iter__(self):
        """
        Get the iterator for the deck.

        >>> deck = Deck()
        >>> deck.shuffle()
        >>> c = [i for i in deck]
        >>> len(c)
        52

        """
        return self.deal
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()    
