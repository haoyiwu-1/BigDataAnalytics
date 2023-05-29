# Importing the argparse library and the pandas library
import argparse
import pandas as pd

# Creating the parser to be used
parser = argparse.ArgumentParser()

# Adding arguments to match the needed command line arguments
# Argument for the file or filename or filepath
parser.add_argument('filepath', type = str)
# Argument for the city
parser.add_argument('city', type = str)
# Argument for the state
parser.add_argument('ST' , type = str)

# Parsing the argument
args = parser.parse_args()

# Setting variables arguments
filepath = args.filepath  # variable for filepath
city = args.city  # variable for city
state = args.ST  # variable for ST / state

# Get data into dataframe using pandas by reading json file
# Given that the format of the json file is a json object per line
# I use lines = True to specify this case
df = pd.read_json(filepath, lines = True)


def getNumberOfBusinesses(input):
    # Function to get the number of businesses in a city
    '''
    Access / check rows based on the city column and the state column where they are 
    equal to both the inputted city and state values from the command line, 
    counting the values only from the city column with the '.city' using 
    .count() to get the total number of businesses in the city
    '''
    # Get all businesses from dataset where city and column values are equal
    # to the inputted city and state from the command line
    numberOfBusinesses = input.loc[(input['city'] == city) & (input['state'] 
    == state)].city.count()

    # Return number of businesses in the city, state 
    # No rounding needed as whole number for business count (not an average)
    return str(numberOfBusinesses)


def getAverageStarsOfBusinesses(input):
    # Function to get average number of stars of businesses in a city
    '''
    Access / check rows based on the city column and the state column where they 
    are the same as both the inputted city and state values from the command 
    line, getting the mean of only the values from the stars column with 
    '.stars' using .mean() to get the mean / average stars of businesses in 
    the city
    '''
    averageStars = input.loc[(input['city'] == city) & 
    (input['state'] == state)].stars.mean()

    # Return average stars of businesses in the city, state
    # Rounding the value as wanted to 2 decimal places using the round()
    # This is because this is an average so rounding is needed
    return str(round(averageStars, 2))


def getNumberOfRestaurants(input):
    # Function to get the number of restaurants in a city
    '''
    Access / check rows based on the categories column by checking if the category of 
    the row contains 'Restaurants' to grab all restaurants. Then keep only the 
    correct restaurants with the right city and state values based on the city
    and state columns as done previously. Finally, once again count the values
    only from the categories column with '.categories' using .count() to get
    the total number of restaurants in the city
    '''
    # First get all restaurants in the dataset from set of all businesses
    numberOfRestaurants = input.loc[input['categories'].str.contains
    ('Restaurants', na = False)]
    # Reduce to only restaurants in the wanted city, state and count
    numberOfRestaurants = numberOfRestaurants.loc[(input['city'] == city) & 
    (input['state'] == state)].categories.count()

    # Return number of restaurants in the city, state 
    # No rounding needed as whole number for restaurant count (not an average)
    return str(numberOfRestaurants)


def getAverageStarsOfRestaurants(input):
    # Function to get average number of stars of restaurants in a city
    '''
    Access / check rows based on the categories column by checking if the category of 
    the row contains 'Restaurants' to grab all restaurants. Then keep only the 
    correct restaurants with the right city and state values based on the city
    and state columns as done previously. Finally, once again get the mean 
    of the values only from the stars column with '.stars' using .mean() to get
    the mean / average stars of restaurants in the city
    '''
    # First get all restaurants in dataset from set of all businesses
    averageStars = input.loc[input['categories'].str.contains
    ('Restaurants', na = False)]
    # Reduce to only restaurants in city, state and get mean of stars
    averageStars = averageStars.loc[(input['city'] == city) & 
    (input['state'] == state)].stars.mean()

    # Return average stars of restaurants in the city, state
    # Rounding the value as wanted to 2 decimal places using the round()
    # This is because this is an average so rounding is needed
    return str(round(averageStars, 2))
    

def getAverageNumberOfReviewsOfBusinesses(input):
    # Function to get average number of reviews of businesses in a city
    '''
    Access / check rows based on the city column and the state column where they are 
    equal to both the inputted city and state values from the command line, 
    get the mean of the values only from the review_count column with 
    '.review_count' using .mean() to get the mean / average number of reviews for 
    businesses in the city
    '''
    averageReviews = input.loc[(input['city'] == city) & (input['state']
    == state)].review_count.mean()

    # Return average number of reviews for businesses in the city, state
    # Rounding the value as wanted to 2 decimal places using the round()
    # This is because this is an average so rounding is needed
    return str(round(averageReviews, 2))


def getAverageNumberOfReviewsOfRestaurants(input):
    # Function to get average number of reviews of restaurants in a city
    '''
    Access /check rows based on the categories column by checking if the category of 
    the row contains 'Restaurants' to grab all restaurants. Then keep only the 
    correct restaurants with the right city and state values based on the city
    and state columns as done previously. Finally, get the mean of the values 
    only from the review_count column with '.review_count' using .mean() to get
    the mean / average number of reviews for restaurants in the city
    '''
    # First get all restaurants in dataset from set of all businesses
    averageReviews = input.loc[input['categories'].str.contains
    ('Restaurants', na = False)]
    # Reduce to only restaurants in city, state and get mean of review_count
    averageReviews = averageReviews.loc[(input['city'] == city) &
    (input['state'] == state)].review_count.mean()

    # Return average number of reviews for restaurants in the city, state
    # Rounding the value as wanted to 2 decimal places using the round()
    # This is because this is an average so rounding is needed
    return str(round(averageReviews, 2))

# List to hold all answers calculated using functions
answers = []

# Adding answers to answer list obtained from the above functions
answers.append(getNumberOfBusinesses(df))
answers.append(getAverageStarsOfBusinesses(df))
answers.append(getNumberOfRestaurants(df))
answers.append(getAverageStarsOfRestaurants(df))
answers.append(getAverageNumberOfReviewsOfBusinesses(df))
answers.append(getAverageNumberOfReviewsOfRestaurants(df))

# Writing answers from answer list to output file
with open('Q1.out', 'w') as f:
    for answer in answers:
        f.write(answer + "\n")
# Closing file after writing
f.close()