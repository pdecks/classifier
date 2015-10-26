"""Loops over all entries (here Yelp reviews) and uses the classifier to get
a best guess at the classification. It shows this best guess to the user and
then asks what the correct category should have been. When run with a new
classifier, the guesses will at first be random, but they should improve
over time.

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


# def read(data, classifier):
#     """Opens data, structured as dictionary, and classifies each entry."""
#     for entry in data['entries']:


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
