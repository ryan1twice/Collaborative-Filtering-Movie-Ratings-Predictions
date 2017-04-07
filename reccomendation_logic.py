from database import *
import csv
from getRatings import *
from scipy.spatial import distance
from math import*

user_obj = [users() for i in range(12)]  # list of
user_obj = user  # copy info from getRatings.py

#caclulate the raw average for the baseline prediction
def raw_average(userClass):
    number_of_ratings = 0
    sum = 0
    for i in range(0,len(userClass),1):
        for rating in userClass[i].movie_ratings:
            if (rating>0): #only add movies that are rated
                sum += rating
                number_of_ratings += 1
    rawAvg = round(float(sum)/float(number_of_ratings),1)
    return rawAvg

def user_bias(userNum):
    user_obj = user  # copy info from getRatings.py
    number_of_ratings = 0
    sum = 0
    for rating in user_obj[userNum].movie_ratings:
        if (rating>0):
            sum += rating
            number_of_ratings += 1
    #Subtract the raw avg from the avg movie score for user
    return (round(float(sum)/float(number_of_ratings),2)) - raw_average(user_obj)

def movie_bias(movieNum):
    user_obj = user  # copy info from getRatings.py
    number_of_ratings = 0
    sum = 0
    # run through each users rating for specific movie
    for i in range(0,len(user_obj),1):
        if (user_obj[i].movie_ratings[movieNum]>0):
            sum += user_obj[i].movie_ratings[movieNum]
            number_of_ratings += 1
    #Subtract the raw avg from the avg movie score for user
    return (round(float(sum)/float(number_of_ratings),2)) - raw_average(user_obj)

#create bias matrix
bias_obj = [users() for i in range(12)]
for j in range(0,12,1):
    for i in range(0,10,1):
        rating = round(raw_average(user_obj) + user_bias(j) + movie_bias(i),1)
        if (rating>5.0): #cant have a higher rating than 5
            rating = 5.0
        if (rating<1.0): #or lower than 1
            rating = 1.0
        bias_obj[j].addRating(rating)

#create baseline error matrix
baseline_error_obj = [users() for i in range(12)]
for j in range(0,12,1):
    for i in range(0,10,1):
        if (user_obj[j].movie_ratings[i]<0):
            err_rating = 9999
        else:
            err_rating = round(user_obj[j].movie_ratings[i] - bias_obj[j].movie_ratings[i],1)
        baseline_error_obj[j].addRating(err_rating)

def userCosineSimilarity(list1,list2):
    both_rated = [] #create a list of the indices both rated
    #same vector
    if (list1 == list2):
        return 0
    for i in range(0,10,1):
        # 9999 value for movies not rated, so checking here
        if (list1[i]<5.0) and (list2[i]<5.0):
            both_rated.append(i)

    numerator = 0
    for index in both_rated:
        numerator += list1[index]*list2[index]

    denominator1 = 0
    denominator2 = 0
    for index in both_rated:
        denominator1 += list1[index]*list1[index]
        denominator2 += list2[index]*list2[index]
    denominator = sqrt(denominator1)*sqrt(denominator2)

    return round(numerator/float(denominator),3)

#create a list of objects for the cosine similarity matrix
cosine_objs = [users() for i in range(12)]
cosine_objs = baseline_error_obj
for j in range(0,12,1):
    for i in range(0,12,1):
        sim = userCosineSimilarity(baseline_error_obj[j].movie_ratings, baseline_error_obj[i].movie_ratings)
        cosine_objs[j].addSimilarity(sim)


def nearestNeighbor(userClass):
    maxVal = 0
    for value in userClass.similarity_angle:
        if abs(value) > abs(maxVal):
            maxVal = value
    return maxVal



def nearestNeighborIndex(userNum):
    userIndex = cosine_objs[userNum].similarity_angle.index(nearestNeighbor(cosine_objs[userNum]))
    return userIndex


for i in range(0,12,1):
    print "%d:" %(i+1) + "  %d" % (nearestNeighborIndex(i)+1)
    #print nearestNeighbor(cosine_objs[i])




#neighborhood predictor
predictor_objs = [users() for i in range(12)]
for userID in range(0,12,1):
    for i in range(0,10,1):
        base_predic = bias_obj[userID].movie_ratings[i]
        neighb = nearestNeighborIndex(userID) #find neighbor
        if (cosine_objs[userID].similarity_angle[neighb] > 0):
            errorRating = baseline_error_obj[neighb].movie_ratings[i]
            if (errorRating < 10): #check for 9999
                predictor_objs[userID].addRating(round(base_predic + errorRating, 1))
            else: #neighbor didnt rate movie
                predictor_objs[userID].addRating(round(base_predic + 0, 1))

        elif (cosine_objs[userID].similarity_angle[neighb] < 0): #dissimilar
            errorRating = baseline_error_obj[neighb].movie_ratings[i]
            if (errorRating < 10):  # check for 9999
                predictor_objs[userID].addRating(round(base_predic + errorRating, 1))
            else:  # neighbor didnt rate movie
                predictor_objs[userID].addRating(round(base_predic + 0, 1))




#Calculating RMSE
def calcRMSE(userClass):
    sum = 0
    movies = 0
    for i in range(0,12,1):
        for rating in userClass[i].movie_ratings:
            #ignore movies not rated (-1)
           if (rating > 0):
               diff = rating - raw_average(userClass)
               sum += diff*diff
               movies += 1
    return sqrt((sum/movies))

print calcRMSE(user_obj)
print calcRMSE(bias_obj)
print calcRMSE(predictor_objs)





ofile = open('similarityMatrix.csv','wb')
writer = csv.writer(ofile)
for i in range(0,12,1):
    writer.writerow(cosine_objs[i].similarity_angle)

ofile.close()

'''
#print bias table
index = 0
print "User:" + "  Bias " + "    Movie: " + " Bias"
print "-----------------------------"
for i in range(0, 12, 1):  # (i=0;i<10;i++)  print user number and their ratings
    if (i<10): #only 10 movies
        print '%3s)'%(i + 1)+" %6s"%user_bias(i)+'    %6s)'%(i + 1)+"%6s"%movie_bias(i)
    else:
        print '%3s)' % (i + 1) + " %6s" % user_bias(i)
'''

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

'''
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
'''

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





print "\nAverage Movie Ratings"

#printRatingsTable(movie_list)

print "Matrix of User Ratings"
printUserRatings(user_obj)

print "Movies Users Have Not Seen"
#printUserNotSeen(user_obj)

print "baseline error"
printUserRatings(baseline_error_obj)

print "baseline prediction"
printUserRatings(bias_obj)

print "final predictions"
printUserRatings(predictor_objs)

#printMovieSimilarity(cosine_sim_obj)
#printUserRatings(bias_obj)
#printUserRatings(baseline_error_obj)
#printUserRatings(user_obj)
#printGraphRatings(user_obj)
#printUserSimilarity(user_obj)
#printUserNotSeen(user_obj)
#printRatingsTable(movie_list)
#printUserRatings(predictor_objs)


