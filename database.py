import requests
from bs4 import BeautifulSoup

class movies():
    '''
    Database with all movie info/ratings
    Prints the data with formatting
    '''
    def __init__(self):
        self.name = "NIL"
        self.num_in_list = 0
        self.imdb_rating = 0
        self.rotten_rating = 0
        self.netflix_rating = 0
        self.user_rating = 0
    def print_title(self):
        print "%-34s %-10s %-10s %-10s %-10s " % ("Movie: ", "IMDB", "RottenT", "Netflix", "Users")
        print "-------------------------------------------------------------------------"
    def print_info(self):
        print "%2s. %-30s %-10s %-10s %-10s %-10s " % (self.num_in_list,self.name, self.imdb_rating,
                    self.rotten_rating, self.netflix_rating, self.user_rating)

class users():
    '''
    Database of the users who took a survey to rate the movies
    Contains:
        -user ID number
        -movie ratings
        -distance between other users
        -graph ratings (movie ratings divided by 5)
    '''
    def __init__(self):
        self.number = 0
        self.movie_ratings = []
        self.similarity_angle = []
        self.graph_ratings = []

    def addRating(self, rating):
        self.movie_ratings.append(rating)

    def addSimilarity(self, dist):
        self.similarity_angle.append(dist)

    def addGraph(self, fraction):
        self.graph_ratings.append(fraction)
