from database import *
import requests
import csv
import copy
import re
from bs4 import BeautifulSoup
from mechanize import Browser


movie_list = [movies() for i in range(10)] #list of movie objects

'''
# access netflix ratings
iteration = 0
with open('/Users/ryanhennings/PycharmProjects/collabFiltering/nextflixratings.txt', 'r') as f:
    data = f.readlines()

    for line in data:
        movie_list[iteration].num_in_list = iteration+1
        movie_list[iteration].netflix_rating = line.split()[-1] #last word is the rating
        read_line = line.split()               #split string
        read_line.pop()                        #pop the rating off to get movie name
        movie_name = ' '.join(read_line)
        movie_list[iteration].name = movie_name
        #movie_list[iteration].print_info()
        iteration = iteration + 1


# access Rotten Tomato ratings
for i in range(0,10,1): #(i=0;i<10;i++)
    print "Scrapping RottenTomatoes user ratings for "+movie_list[i].name
    temp_name = movie_list[i].name
    if (movie_list[i].name == "The Interview"): #this movie needs year in address
        temp_name = temp_name.replace(" ", "_")  # replace spaces with underscore for url address
        url = "http://www.rottentomatoes.com/m/" + temp_name + "_" + "2014"
        print url
    elif (i == 2): #benchwarmers doesnt have "the"
        url = "http://www.rottentomatoes.com/m/" + "benchwarmers"
        print url
    else:  #other movies work fine
        temp_name = temp_name.replace(" ", "_")  # replace spaces with underscore for url address
        url = "http://www.rottentomatoes.com/m/" + temp_name
        print url

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    get_rt_rating = soup.find('div', {'class': 'meter-value'})
    rt_rating = get_rt_rating.text
    print "Rating: " + rt_rating
    rt_rating = rt_rating.replace('%','')
    rt_rating = float(rt_rating)
    rt_rating = rt_rating/float(10)  #convert to 5 star base
    rt_rating = rt_rating/float(2)
    rt_rating = round(rt_rating, 1)  #round to one decimal
    movie_list[i].rotten_rating = rt_rating

print "DONE SCRAPPING ROTTEN TOMATOES"+'\n'

# access IMDB ratings
base_url = "http://www.imdb.com"
for i in range(0,10,1): #(i=0;i<10;i++)
    print "Searching IMDB to find "+movie_list[i].name
    temp_name = movie_list[i].name
    temp_name = temp_name.replace(" ", "+") #IMDB take + as spaces in search
    br = Browser()
    url = '%s/find?ref_=nv_sr_fn&q=%s' % (base_url,temp_name)
    print url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    get_r = soup.find('td', {'class': 'result_text'})
    get_r = str(get_r)     #convert to string to insert link
    #print get_r
    get_r = re.findall(r'"(.*?)"', get_r)
    get_r.pop(0)    #pop off the 'result_text'
    temp_name = ''.join(get_r)  #convert list to string
    print "Scrapping IMDB page user ratings for "+movie_list[i].name
    print '%s%s' % (base_url,temp_name) #should be link to movie page
    url = base_url+temp_name
    r = requests.get(url) #opens up the movie page
    soup = BeautifulSoup(r.content, "html.parser")
    get_imdb_r = soup.find('span', {'itemprop':'ratingValue'})
    imdb_r = get_imdb_r.text
    print "Rating: " + imdb_r
    imdb_r = float(imdb_r)
    imdb_r = imdb_r/float(2)
    imdb_r = round(imdb_r, 1)
    movie_list[i].imdb_rating = imdb_r

print "DONE SCRAPPING IMDB"+'\n'

#import user ratings (average)

def getUserRatings(userClass):
    user = [users() for i in range(12)]  # create list of users objects
    f = open('/Users/ryanhennings/PycharmProjects/collabFiltering/formResponses.csv')
    csvfile = csv.reader(f)
    index = 0
    for row in csvfile:
        user[index].number = index + 1
        uRatings = row
        uRatings.pop(0)  # pop timestamp off
        for stars in uRatings:  # pop "stars" off each
            uStars = stars.replace("stars", "")
            uStars = uStars.replace("star", "")
            uStars = uStars.replace("Have not seen", "-1")

            user[index].addRating(uStars)
        index = index + 1
    return user

'''

f = open('/Users/ryanhennings/PycharmProjects/collabFiltering/formResponses.csv')
csvfile = csv.reader(f)
user = [users() for i in range(12)] #list of users
user2 = [users() for i in range(12)] #list of users
index = 0
for row in csvfile:
    user[index].number = index+1
    uRatings = row
    uRatings.pop(0) #pop timestamp off
    for stars in uRatings: #pop "stars" off each
        uStars = stars.replace("stars","")
        uStars = uStars.replace("star","")
        uStars = uStars.replace("Have not seen","-1")

        uStars = uStars.replace(" ","")
        user[index].addRating(int(uStars))
        user2[index].addRating(uStars)
    index = index+1

size = len(user) #store how many users

#Get average user ratings
for j in range(0,10,1): #(i=0;i<10;i++)
    sum = 0
    counter = 0

    for i in range(0,size,1): #(i=0;i<size;i++)
        if (float(user[i].movie_ratings[j])==-1):
            counter = counter+1     #need to count number of people who havent seen the movie
        else:
            sum = sum + float(user[i].movie_ratings[j])

    average = sum/float(size-counter)
    average = round(average, 1)
    movie_list[j].user_rating = average

'''
    Functions for printing the data
    Include:
        -user ratings matix
        -user ratings matrix with only movies that have not been seen
        -movie ratings table from all sources

'''
# Top title formating for printing User matrices
def printUserMatrixTitle():
    nums = []  # create a list 1-10 for movie number in matrix
    nums.extend(range(1, (size-1)))
    print '%-4s|' % (' ') + ' '.join('%6s' % str(x) for x in nums)  # print x axis of matrix title
    # seperate matrix info
    print "---------------------------------------------------------------------------"

# format matrix with all values for printing
def printUserRatings(userClass):
    printUserMatrixTitle()
    for i in range(0, size, 1):  # (i=0;i<10;i++)  print user number and their ratings
        print '%-4s|' % (i + 1) + '%s' % ' '.join('%6s' % val for val in userClass[i].movie_ratings)
    print '\n'

#print user ratings for graph
def printGraphRatings(userClass):
    printUserMatrixTitle()
    for i in range(0, size, 1):  # (i=0;i<10;i++)  print user number and their ratings
        print '%-4s|' % (i + 1) + '%s' % ' '.join('%6s' % val for val in userClass[i].graph_ratings)
    print '\n'

# second matrix just to show movies with no ratings
def printUserNotSeen(userClass):
    printUserMatrixTitle()
    for i in range(0, size, 1):
        ratings_to_ints = map(int, user2[i].movie_ratings)  # convert strings in list to ints
        proccessed_nums = [(' ' if num > 0 else num) for num in ratings_to_ints]  # replace ratings with ' '
        user2[i].movie_ratings = proccessed_nums
    for i in range(0, size, 1):  # (i=0;i<10;i++)  print user number and their ratings
        print '%-4s|' % (i + 1) + '%s' % ' '.join('%6s' % val for val in user2[i].movie_ratings)
    print '\n'

# similarity matrix between users
def printUserSimilarity(userClass):
    # Tite formatting
    nums = []  # create a list 1-10 for movie number in matrix
    nums.extend(range(1,13))
    print "Table of Similarity Values (cosine angle)"
    print '%-4s|' % (' ') + ' '.join('%7s' % str(x) for x in nums)  # print x axis of matrix title
    # seperate matrix info
    print "-----------------------------------------------------------------------------------------------------"
    # user similarity
    for i in range(0, size, 1):  # (i=0;i<10;i++)  print user number and their ratings
        print '%-4s|' % (i + 1) + '%s' % ' '.join('%7s' % val for val in userClass[i].similarity_angle)
    print '\n'

def printMovieSimilarity(userClass):
    # Tite formatting
    nums = []  # create a list 1-10 for movie number in matrix
    nums.extend(range(1, 11))
    print
    print '%-4s|' % (' ') + ' '.join('%8s' % str(x) for x in nums)  # print x axis of matrix title
    # seperate matrix info
    print "-----------------------------------------------------------------------------------------------"

    # user similarity
    for i in range(0, 10, 1):  # (i=0;i<10;i++)  print user number and their ratings
        print '%-4s|' % (i + 1) + '%8s' % ' '.join('%8s' % val for val in userClass[i].movie_ratings)
    print '\n'


#print list of movies and ratings
def printRatingsTable(moviesClass):
    print_top = movies()
    print_top.print_title()
    for i in range(0, 10, 1):  # (i=0;i<10;i++)
        moviesClass[i].print_info()
    print '\n'

'''
printUserRatings(user)
printUserNotSeen(user)
printRatingsTable(movie_list)
'''

#movie_list2 = copy.deepcopy(movie_list) #for copying list info to another object


