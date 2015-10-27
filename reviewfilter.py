"""Loops over all entries (here Yelp reviews) and uses the classifier to get
a best guess at the classification. It shows this best guess to the user and
then asks what the correct category should have been. When run with a new
classifier, the guesses will at first be random, but they should improve
over time.

>>> import docclass
>>> import reviewfilter as rf
>>> c1 = docclass.FisherClassifier(docclass.getwords)
>>> c1.setdb('pdecks_reviews.db')
>>> my_dir = '/Users/pdecks/hackbright/project/Yelp/pdecks-reviews/'
>>> filelist = rf.generate_filelist(my_dir)
>>> my_reviews = rf.generate_review_dict(filelist)

by: Patricia Decker, modified from Programming Collective Intelligence
date: 10/26/2015
"""

import os
import glob
my_dir = '/Users/pdecks/hackbright/project/Yelp/pdecks-reviews/'

def generate_filelist(my_dir):
    """Takes a directory path and returns a list of text files in directory."""
    filelist = []
    os.chdir(my_dir)
    for files in glob.glob("*.txt"):
        filelist.append(files)
    return filelist

def generate_business_dict(filename):
    """Given a filename, make a dictionary entry"""
    review_dict = {}

    review_file = open(filename)
    review_data = review_file.read()

    # extract review data, splitting on pipes
    current_review = review_data.split("|")

    # assign meaningful variable names
    rest_name = current_review[0]
    rest_score = current_review[1]
    review_date = current_review[2]
    review_text = current_review[3]

    # assign values to dictionary keys
    review_dict['name'] = rest_name
    review_dict['score'] = int(rest_score)
    review_dict['date'] = review_date
    review_dict['review'] = review_text

    review_file.close()

    return review_dict


def generate_review_dict(filelist):
    """Takes a list of files (reviews) and returns a dictionary of reviews."""
    my_reviews = {}

    for business in filelist:
        # make the dictionary entry for current business
        business_dict = generate_business_dict(business)

        # add to larger review dictionary
        business_name = business_dict['name']
        my_reviews[business_name] = business_dict

    return my_reviews


def classify_reviews(review_dict, classifier):
    """Takes a dictionary of reviews and classifies the entries."""
    print "In classify_reviews ..."
    for entry in review_dict:

        print '-' * 60
        print "Business name: %s" % review_dict[entry]['name']
        print "Score: %s" % review_dict[entry]['score']
        print "Review date: %s" % review_dict[entry]['date']
        print "Review: %s" % review_dict[entry]['review']
        print '-' * 60

        # combine all the text to create one item for the classifier
        fulltext = '%s\n%s\n%s\n%s' % (review_dict[entry]['name'],
                                       review_dict[entry]['score'],
                                       review_dict[entry]['date'],
                                       review_dict[entry]['review'])
        # print fulltext

        # print the best guess at the current category
        print 'Guess: ' + str(classifier.classify(fulltext))

        # Ask the user to specify the correct category and train on that
        user_cat = raw_input('Enter category: ')
        classifier.train(fulltext, user_cat)


if __name__ == "__main__":
    filelist = generate_filelist(my_dir)
    my_reviews = generate_review_dict(filelist)
    print '\n\n'
    print "RESTAURANTS REVIEWED"
    for restaurant in my_reviews.keys():
        print restaurant
    print '\n\n'
    print '-'*60

    for review in my_reviews:
        print "%s" % review
        print my_reviews[review]
        print '-'*60

# import docclass
# import reviewfilter as rf
# c1 = docclass.FisherClassifier(docclass.getwords)
# c1.setdb('pdecks_reviews.db')
# my_dir = '/Users/pdecks/hackbright/project/Yelp/pdecks-reviews/'
# filelist = rf.generate_filelist(my_dir)
# my_reviews = rf.generate_review_dict(filelist)
# rf.classify_reviews(my_reviews, c1)


## DEBUGGING

# print "This is entry['name']: %s" % review_dict[entry]['name']
# print "This is entry['score']: %s" % review_dict[entry]['score']
# print "This is entry['date']: %s" % review_dict[entry]['date']
