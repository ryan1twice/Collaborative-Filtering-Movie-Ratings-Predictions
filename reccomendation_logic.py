from database import *
from getRatings import *
from scipy.spatial import distance
from math import sqrt

user_obj = [users() for i in range(12)]  # list of
user_obj = user  # copy info from getRatings.py


# score of distance between the user scores
def eulidean_distance(user1, user2):
    # type: (object, object) -> object
    user_obj = [users() for i in range(12)]  # list of
    user_obj = user  # copy info from getRatings.py

    user1_seen = []
    user2_seen = []
    both_seen = []
    user1_compare_ratings = []
    user2_compare_ratings = []
    index = 0
    # get a list of movies user 1 has seen
    for item in user_obj[user1].movie_ratings:
        if (item > 0):
            user1_seen.append(index)
        index += 1

    # get a list of movies user 1 has seen
    index = 0
    for item in user_obj[user2].movie_ratings:
        if (item > 0):
            user2_seen.append(index)
        index += 1
    # get a list of movies both users have seen
    for val in user1_seen:
        if val in user2_seen:
            both_seen.append(val)

    for item in both_seen:
        user1_compare_ratings.append(user_obj[user1].movie_ratings[item])

    for item in both_seen:
        user2_compare_ratings.append(user_obj[user2].movie_ratings[item])

    return distance.euclidean(user1_compare_ratings, user2_compare_ratings)


def cosine_distance(user1, user2):
    user_obj = [users() for i in range(12)]  # list of
    user_obj = user  # copy info from getRatings.py

    user1_seen = []
    user2_seen = []
    both_seen = []
    user1_compare_ratings = []
    user2_compare_ratings = []
    index = 0
    # get a list of movies user 1 has seen
    for item in user_obj[user1].movie_ratings:
        if (item > 0):
            user1_seen.append(index)
        index += 1

    # get a list of movies user 1 has seen
    index = 0
    for item in user_obj[user2].movie_ratings:
        if (item > 0):
            user2_seen.append(index)
        index += 1
    # get a list of movies both users have seen
    for val in user1_seen:
        if val in user2_seen:
            both_seen.append(val)

    for item in both_seen:
        user1_compare_ratings.append(user_obj[user1].movie_ratings[item])

    for item in both_seen:
        user2_compare_ratings.append(user_obj[user2].movie_ratings[item])

    return distance.cosine(user1_compare_ratings, user2_compare_ratings)

# Distance similarity between users
for usr1 in range(0, 12, 1):
    for usr2 in range(0,12,1):
        #round distance to 2 decimals
        sim_dist = round(eulidean_distance(usr2,usr1), 2)
        #add the distance to the user object
        user_obj[usr2].addSimilarity(sim_dist)
    #print "%.4s" % eulidean_distance(0, j)

# Divide user ratings by 5 (0.2,0.4,0.6...) for calculating graph path distance
for i in range(0,len(user_obj)):
    for j in range(0,len(user_obj[1].movie_ratings),1):
        if (user_obj[i].movie_ratings[j] > 0):
            user_obj[i].addGraph(float((user_obj[i].movie_ratings[j])/5.0))
        else:
            user_obj[i].addGraph(0)


printUserRatings(user_obj)
printGraphRatings(user_obj)
printUserSimilarity(user_obj)
printUserNotSeen(user_obj)
printRatingsTable(movie_list)


