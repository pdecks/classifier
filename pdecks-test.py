
import docclass
import reviewfilter as rf
c1 = docclass.FisherClassifier(docclass.getwords)
c1.setdb('pdecks_reviews.db')
my_dir = '/Users/pdecks/hackbright/project/Yelp/pdecks-reviews/'
filelist = rf.generate_filelist(my_dir)
my_reviews = rf.generate_review_dict(filelist)
rf.classify_reviews(my_reviews, c1)