"""
Learns how to classify a document by being trained. Accuracy improves
with continued exposure to new information as classifier learns which
features are important for making a distinction.

from Programming Collective Intelligence, by Toby Segaran.
"""

import re
import math


def sampletrain(c1):
    """Dumps some sample training data into the classifier."""
    c1.train('Nobody owns the water.', 'good')
    c1.train('the quick rabbit jumps fences', 'good')
    c1.train('buy pharmaceuticals now', 'bad')
    c1.train('make quick money at the online casino', 'bad')
    c1.train('the quick brown fox jumps', 'good')


def getwords(doc):
    """Feature extractor.

    Takes a document and splits it on any sequence of non-alphanumeric
    characters. Here, the resulting words are the document features.
    """

    # compiling regular expressions with python built-in library re, a C
    # extension module. Note REs are handled as strings because REs are not
    # part of core Python so no syntax was created for expressing them.

    # RegEx are compiled into PATTERN OBJECTS, thus splitter is a pattern obj
    # note compile('\\W*') is the string literal form
    # the raw string form would be compile(r'\W*')
    splitter = re.compile('\\W*')

    # split the words by non-alpha characters
    # the split() method OF A PATTERN splits a string apart whever the RegEx
    # matches, returning a list of the pieces.
    # below command ignores 2-letter words and words longer than 20 letters
    words = [s.lower() for s in splitter.split(doc)
             if len(s) > 2 and len(s) < 20]

    # return the unique set of words only
    return dict([(w, 1) for w in words])


class Classifier:
    """Encapsulate what the classifier has learned so far. This allows for
    instantiation of multiple classifiers for different users, groups, or
    queries that can be trained to a particular group's needs."""

    def __init__(self, getfeatures, filename=None):
        # Counts of feature/category combinations
        # ex. {'python': {'bad': 0, 'good': 6}, 'the': {'bad': 3, 'good': 3}}
        # where 'python' is a feature and 'bad' and 'good' are categories
        self.fc = {}

        # Counts of documents in each category
        # dict of how many times every classification has been used
        # this is needed for probability calculations
        # ex. # documents labeled 'good' or 'bad' --> {'good': 3, 'bad': 3}
        self.cc = {}

        # Function that will be used to extract the features from items
        # to be classified (ex: getwords)
        self.getfeatures = getfeatures


    ## CREATE HELPER METHODS TO INCREMENT AND GET THE COUNTS ##
    # note that .setdefault() will set d[key]=default IF key not already in d
    # here, if feature not yet in dict, create key
    # then, for each feature dictionary, if category not yet in feature dict,
    # add category as value and set it to 0. THEN, for all cases, increment.

    def incf(self, f, cat):
        """Increases the count of a feature/category pair."""
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1


    def incc(self, cat):
        """Increase the count of a document category (classification)."""
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1


    def fcount(self, f, cat):
        """Returns a float of no. times a feature has appeared in a category."""
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0


    def catcount(self, cat):
        """Returns a float of no. times a category occurs as a classification."""
        if cat in self.cc:
            return float(self.cc[cat])
        return 0


    def totalcount(self):
        """Returns total number of all category (classification) occurrences."""
        return sum(self.cc.values())


    def categories(self):
        """Returns list of all categories (classifications)."""
        return self.cc.keys()


    ## TRAIN THE MODEL ##

    def train(self, item, cat):
        """Takes an item (e.g., document) and a classification.
        Increments counters."""

        # extract the features
        features = self.getfeatures(item)

        # increment the count for every feature with this category
        for f in features:
            self.incf(f, cat)

        # increment the count for this category
        self.incc(cat)


    ## CALCULATING PROBABILITIES
    def fprob(self, f, cat):
        """Returns conditional probability P(A|B) = P(word|classification).

        >>> import docclass
        >>> c1 = docclass.Classifier(docclass.getwords)
        >>> docclass.sampletrain(c1)
        >>> c1.fprob('quick', 'good')
        0.6666666666666666
        """
        if self.catcount(cat) == 0: return 0

        # the total number of times this feature appeared in this category
        # divided by the total number of items in this category
        return self.fcount(f, cat) / self.catcount(cat)


    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        """Returns a weighted average of getprobability and assumed
        probability.

        prf = probability function
        ap = assumed probability
        """

        # calculate current probability
        basicprob = prf(f, cat)

        # count the number of times this feature has appeared in all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])

        # calculate the weighted average
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)

        return bp


## Test the class using python interactively ##
# import docclass
# c1 = docclass.Classifier(docclass.getwords)
# docclass.sampletrain(c1)
# c1.fcount('quick', 'good') --> returns 1.0
# c1.fcount('quick', 'bad') --> returns 1.0
