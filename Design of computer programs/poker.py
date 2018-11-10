import random

def poker(hands):
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    # Your code here.
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result


def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

# old hank rank

"""def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

"""
def hand_rank(hand):
    #counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1); ranks = (7, 8, 9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
       ranks == (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    #return(9 if (5,) == counts else
      #  8 if straight and flush else
       # 7 if (4, 1) == counts else
       # 6 if (3, 2) == counts else
       # 5 if flush else
       # 4 if straight else
       # 3 if (3,1,1) == counts else
       # 2 if (2,2,1) == counts else
       # 1 if (2,1,1,1) == counts else
       # 0), ranks
    return max(count_rankings[counts], 4*straight + 5*flush), ranks
        


count_rankings = {(5, ): 10, (4,1): 7, (3,2):6, (3,1,1):3, (2,2,1):2,
 (2,1,1,1):1, (1,1,1,1,1):0}
def group(items):
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs): return zip(*pairs)

def two_pair(ranks):
    "If there are two pair here, return the two ranks of the two pairs, else None."
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

    

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks


def deal(numhands, n = 5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def hand_percentages(n=700*10):
    counts = [0] * 9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    #for i in reversed(range(9)):
       # print "%14s: %6.3f %%" % (hand_names[i], 100 * counts[i]/n)
def test():
    sf = "6C 7C 8C 9C TC".split()
 
    assert poker([sf]) == [sf]

    "Test cases"
    rf = "KS AS QS TS JS".split()
    rf_too = "KD AD QD TD JD".split()
    straight_flush = "5C 6C 7C 8C 9C".split()
    four_kind = "AD AS AC AH 8C".split()
    four_kind_too = "KD KS KC KH 8C".split()
    four_kind_twee = "KD KS KC KH 7C".split()
    full_house = "KH KC KS TH TC".split()
    full_house_too = "AH AC AS JH JC".split()
    flush = "QC 6C 4C 3C 8C".split()
    flush_too = "QC TC 4C 3C 8C".split()
    straight = "2S 3C 4S 5H 6H".split()
    straight_too = "2S 3C 4S 5H AH".split()
    three_kind = "JS JH JC 5C 8D".split()
    two_pair = "TS TH 6S 6C KC".split()
    one_pair = "AH AC 8D 6H 2S".split()
    high_card = "KH JS TC 6H 3D".split()
    high_card_too = "KH JS 9C 6H 3D".split()
    #print max([3,4,5,6]), max([3,4,-5], key=abs)

    assert kind(4, four_kind) == None

    assert poker([straight_flush, four_kind, full_house]) == [straight_flush]
    assert poker([flush, straight, three_kind]) == [flush]
    assert poker([two_pair, one_pair, high_card]) == [two_pair]
    assert poker([straight, straight_too]) == [straight]
    assert poker([straight_too, straight]) == [straight]

    assert poker([rf, straight_flush]) == [rf]
    assert poker([straight_flush, rf]) == [rf]
    assert poker([four_kind_twee, four_kind, four_kind_too]) == [four_kind]
    assert poker([four_kind_too, four_kind_twee]) == [four_kind_too]
    assert poker([four_kind_twee, four_kind_too]) == [four_kind_too]
    assert poker([full_house, full_house_too]) == [full_house_too]
    assert poker([full_house_too, full_house]) == [full_house_too]
    assert poker([flush, flush_too]) == [flush_too]
    assert poker([flush_too, flush]) == [flush_too]
    assert poker([high_card, high_card_too]) == [high_card]
    assert poker([high_card_too, high_card]) == [high_card]

    assert poker([flush, straight_flush, straight,
                    high_card, two_pair, four_kind,
                    three_kind, one_pair]) == [straight_flush]

    assert sorted(poker([rf, rf_too])) == sorted([rf, rf_too])
    return "tests pass"

print deal(2,7)
test()

