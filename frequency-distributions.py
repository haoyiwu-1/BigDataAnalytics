# Importing needed libraries
import argparse
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Creating the parser to be used
parser = argparse.ArgumentParser()

# Adding arguments to match the needed command line arguments
# Argument for the file / filename / filepath
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

# Grabbing all rows which contain 'restaurant' in its categories
restaurants = df.loc[df['categories'].str.contains('Restaurants', na = False)]
# Further reducing rows based on restaurants only in the wanted city and state
restaurants = restaurants.loc[(restaurants['city'] == city) & 
            (restaurants['state'] == state)]
# Removing all other columns except for categories and review count
restaurants = restaurants[['categories', 'review_count']]

# common cuisines found online
# From two websites
# https://blog.yelp.com/businesses/yelp_category_list/#section21
# https://towardsdatascience.com/analyzing-worldwide-cuisines-with-python-and-foursquare-api-e63455c14246
# Any duplicates from both lists were removed but any additional ones were kept
common_cuisine_dict = {
    'Afghan': 0, 'African': 0,
    'Senegalese': 0, 'South African': 0,
    'American (New)': 0, 'American (Traditional)': 0,
    'Arabian': 0, 'Argentine': 0,
    'Armenian': 0, 'Asian Fusion': 0,
    'Australian': 0, 'Austrian': 0,
    'Bangladeshi': 0, 'Basque': 0,
    'Belgian': 0, 'Brazilian': 0,
    'British': 0, 'Bulgarian': 0,
    'Burmese': 0, 'Cajun/Creole': 0,
    'Cambodian': 0, 'Caribbean': 0,
    'Dominican': 0, 'Haitian': 0,
    'Puerto Rican': 0, 'Trinidadian': 0,
    'Catalan': 0, 'Chinese': 0, 
    'Cantonese': 0, 'Hainan': 0,
    'Shanghainese': 0, 'Szechuan': 0,
    'Cuban': 0, 'Czech': 0,
    'Eritrean': 0, 'Ethiopian': 0,
    'Filipino': 0, 'French': 0,
    'Mauritius': 0, 'Reunion': 0,
    'Georgian': 0, 'German': 0,
    'Greek': 0, 'Guamanian': 0,
    'Hawaiian': 0, 'Himalayan/Nepalese': 0,
    'Honduran': 0, 'Hungarian': 0,
    'Iberian': 0, 'Indian': 0,
    'Indonesian': 0, 'Irish': 0,
    'Italian': 0, 'Calabrian': 0,
    'Sardinian': 0, 'Sicilian': 0,
    'Tuscan': 0, 'Korean': 0,
    'Laotian': 0, 'Latin American': 0,
    'Colombian': 0, 'Salvadoran': 0,
    'Venezuelan': 0, 'Malaysian': 0,
    'Mediterranean': 0, 'Mexican': 0,
    'Middle Eastern': 0, 'Egyptian': 0,
    'Lebanese': 0, 'Modern European': 0,
    'Mongolian': 0, 'Moroccan': 0, 
    'New Mexican Cuisine': 0, 'Nicaraguan': 0,
    'Pakistani': 0, 'Pan Asia': 0,
    'Persian/Iranian': 0, 'Peruvian': 0,
    'Polish': 0, 'Polynesian': 0,
    'Portuguese': 0, 'Russian': 0,
    'Scandinavian': 0, 'Scottish': 0,
    'Singaporean': 0, 'Slovakian': 0,
    'Somali': 0, 'Southern': 0,
    'Spanish': 0, 'Sri Lankan': 0,
    'Syrian': 0, 'Taiwanese': 0,
    'Thai': 0, 'Turkish': 0, 
    'Ukrainian': 0, 'Uzbek': 0, 
    'Vietnamese': 0, 'Japanese': 0, 
    'Malay': 0, 'Tibetan': 0, 
    'Caucasian': 0, 'Dutch': 0, 
    'Belarusian': 0, 'Bosnian': 0, 
    'Romanian': 0, 'Tatar': 0, 
    'English': 0, 'Argentinian': 0, 
    'Iraqi': 0, 'Israeli': 0, 
    'Kurdish': 0, 'Yemeni': 0, 
    'Swiss': 0, 'Ukranian': 0, 
    'Hakka': 0
}


def getRestaurantDistribution(input):
    # Function to compute frequency distribution of restaurants based
    # on categories which are based on geographical origin

    # Splitting the categories into a list of lists of string categories
    categories = input.categories.str.split(',').tolist()
    '''
    I noticed that most geographical origins of cuisines had 
    common substrings and string endings
    Contains ian
    Ends with ese
    Ends with ish
    Ends with ean
    Contains (
    Ends with ern
    '''
    # For loop to loop through the category lists and categories themselves
    for cat_list in categories:
        for type in cat_list:
            # Cleaning up the category strings
            cuisine = type.strip()
            # To cover cuisines with 'ian' in them
            # Also remove vegan and vegetarian
            if ((('ian' in cuisine) & ('Veg' not in cuisine))
            # To cover cuisines with ese at the end
            or cuisine.endswith('ese') 
            # To cover cuisines with ish at the end
            or cuisine.endswith('ish')
            # To cover cuisines with ean at the end
            or cuisine.endswith('ean')
            # To cover cuisines with ( in them
            or '(' in cuisine
            # To cover cuisines with ern at the end
            or cuisine.endswith('ern') 
            # To cover common cuisines 
            # found from Yelp website and another online source
            or common_cuisine_dict.get(cuisine) == 0):
                # Either add new cuisine to cuisine counter dictionary
                # Or increment an existing value
                if cuisine in cuisine_freq:
                    cuisine_freq[cuisine] += 1
                else:
                    cuisine_freq[cuisine] = 1


def getRestaurantReviewDistribution(input):
    # Function to compute frequency distribution and average of restaurant reviews 
    # based on categories which are based on geographical origin

    # Splitting the categories into a list of lists of string categories
    reviews = input.review_count.values
    # Setting counter variable
    index = 0

    # For loop to loop through the category lists and categories themselves
    for cat_list in input.categories:
        # Splitting categories list to categories
        types = cat_list.split(',')
        for type in types:
            # Cleaning up the category strings
            cuisine = type.strip()
            # To cover cuisines with 'ian' in them
            # Also remove vegan and vegetarian
            if ((('ian' in cuisine) & ('Veg' not in cuisine))
            # To cover cuisines with ese at the end
            or cuisine.endswith('ese') 
            # To cover cuisines with ish at the end
            or cuisine.endswith('ish')
            # To cover cuisines with ean at the end
            or cuisine.endswith('ean')
            # To cover cuisines with ( in them
            or '(' in cuisine
            # To cover cuisines with ern at the end
            or cuisine.endswith('ern') 
            # To cover common cuisines 
            # found from Yelp website and another online source
            or common_cuisine_dict.get(cuisine) == 0):
                # Either add new cuisine to review counter dictionary
                # Or increment an existing value by amount of reviews
                if cuisine in review_freq:
                    review_freq[cuisine] += reviews[index]
                else:
                    review_freq[cuisine] = reviews[index]
        # Increment index to match current restaurant review count
        index += 1


def createBarChart():
    # Function to create bar chart based on top 5 restaurant categories
    # The size will be 10 inches x 10 inches

    # Dictionary created from top ten restaurant categories
    # But having only the top 5
    top_five = dict(Counter(top_ten_cuisines).most_common(5))

    # Adding the top 5 restaurant categories and their freqs to lists
    Top_5_Cuisines = []
    Top_5_Freq = []
    for cuisine, freq in top_five.items():
        Top_5_Cuisines.append(cuisine)
        Top_5_Freq.append(freq)

    # Creating bar chart using matplotlib
    plt.style.use('_mpl-gallery')
    # Making the bar chart 10 inches x 10 inches
    plt.rcParams["figure.figsize"] = (10, 10)
    fig = plt.figure()
    # Adding axes and data based on the lists created before
    ax = fig.add_axes([0, 0, 1, 1])
    bars = ax.bar(Top_5_Cuisines, Top_5_Freq)
    # Setting title for bar chart
    plt.title('Top 5 Restaurant Categories by Frequency', fontsize = 30)
    # Setting x axis for bar chart
    plt.xlabel('Restaurant Category by Cuisine (geographical origin)', fontsize = 20)
    # Setting x axis for bar chart
    plt.ylabel('Frequency (number of restaurants)', fontsize = 20)
    ax.bar_label(bars)
    # Saving bar chart to pdf as wanted
    plt.savefig("Q2_part3.pdf", format = "pdf", bbox_inches = "tight")


# Dictionary / map to keep track of the freqency of restaurants for each 
# restaurant category by geographical origin
cuisine_freq = {}
# Dictionary / map to keep track of the restaurant review freqency 
# for each restaurant category by geographical origin
review_freq = {}
# Dictionary to hold the top ten restaurants by category / cuisine
top_ten_cuisines = {}
# Dictionary to hold the top ten restaurants by category / cuisine based 
# on review frequency
top_ten_cuisines_by_reviews = {}

# Calling functions to get needed distributions
getRestaurantDistribution(restaurants)
getRestaurantReviewDistribution(restaurants)

# Extracting the top ten restaurant categories 
# from the cuisine freq dictionary
top_ten_cuisines = dict(Counter(cuisine_freq).most_common(10))

# Writing the top ten restaurant categories to output file
with open('Q2_part1.out', 'w') as f:
    for cuisine, count in top_ten_cuisines.items(): 
        f.write(cuisine + ":" + str(count) + "\n")
# Closing file after writing
f.close()

# Extracting the top ten restaurant categories by review count
# from the review freq dictionary
top_ten_cuisines_by_reviews = dict(Counter(review_freq).most_common(10))

# Writing the top ten restaurant categories by review count to output file
with open('Q2_part2.out', 'w') as f:
    for cuisine, count in top_ten_cuisines_by_reviews.items():
        f.write(cuisine + ":" + str(count) + ":" + str(round(count / cuisine_freq[cuisine], 2)) + "\n")
# Closing file after writing
f.close()

# Calling function to create bar chart and saving to pdf file
createBarChart()