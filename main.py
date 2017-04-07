from database import *
from getRatings import *

user_obj = [users() for i in range(12)] #list of
movies_obj = [movies() for i in range(10)] #list of movie objects


user_obj = user  #copy info from getRatings.py
movies_obj = movie_list

printRatingsTable(movies_obj)



#printUserRatings(users)

