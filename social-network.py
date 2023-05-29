# Importing needed libraries
import argparse
import pandas as pd
import os


def check_n(value):
    # Function to check if enter value for n is valid
    # Try catch to see if entered n value is an integer or not
    try:
        integer_val = int(value)
    except ValueError:
        # Throw error that entered n value is not an integer
        raise argparse.ArgumentTypeError("Entered n value is not an integer...")
    # Throw error if integer value is smaller than 100
    if integer_val < 100:
            raise argparse.ArgumentTypeError(str(value) +
            " is an invalid integer value for n as " + 
            "it must be greater than or equal to 100...")
    return integer_val

# Creating the parser to be used
parser = argparse.ArgumentParser()

# Adding arguments to match the needed command line arguments
# Argument for the file or filename or filepath
parser.add_argument('filepath', type = str)
# Argument for n
parser.add_argument('n', type = check_n)

# Parsing the argument
args = parser.parse_args()

# Setting variables arguments
filepath = args.filepath  # variable for filepath
n = args.n  # variable n

# Check if output file already exists if it does remove it
if os.path.exists("Q3.out"):
    os.remove("Q3.out")

# List to hold all possible users with 'useful' greater than n
possible_users_list = []

# Grabbing all users with 'useful' >= n
# Get data into dataframe using pandas by reading json file
# Given that the format of the json file is a json object per line
# I use lines = True to specify this case
# As the json file is too large to process all at once
# I need to set a chunk size, I decide to use 25k
# Grab a chunk of 25000 user objects to process
for partition in pd.read_json(filepath, lines = True, chunksize = 25000):
    # Set data to the chunk
    data = partition
    # Get only the rows which have a 'useful' greater than or equal to n
    data = data[data['useful'] >= n]
    # Further reduce the rows to ones which only have friends
    # This is because no friends means no edge so it won't be needed
    data = data[data['friends'].str.contains('None') != True]
    
    # Adding users with 'useful' greater than or equal to n to users_list
    if not data.empty:
        users_sublist = data['user_id'].values.tolist()
        for user in users_sublist:
            possible_users_list.append(user)


# List of all users in graph / edge list
final_users_edge_list = []

# Go through all users again with the same settings
for partition in pd.read_json(filepath, lines = True, chunksize = 25000):
    data = partition
    # Make sure that user_id is in users_list
    data = data.loc[data['user_id'].isin(possible_users_list)]

    # Exploding the friends list to match user_id with friend user_id
    data_transformed = data.assign(friends=data.friends.str.split(',')).explode('friends')
    # Keep only the user_id and friends column
    data_transformed = data_transformed[['user_id', 'friends']]
    # Rename columns to 'user_id' and 'friend'
    data_transformed.columns = ['user_id', 'friend']

    # Make sure only friends that have useful greater than or equal to n are included
    data_transformed = data_transformed.loc[data_transformed['friend'].isin(possible_users_list)]

    # List of values to check for duplicates in partition
    partition_check_values = []

    # Concatenating user_id and friend column lexicographically
    # Therefore, duplicate columns will have the same value when concatenated
    # Then these duplicates can be dropped later
    # Adding these check values to partition_check_values list
    for index, row in data_transformed.iterrows():
        row = ''.join(sorted([row['user_id'], row['friend']]))
        partition_check_values.append(row)

    # Adding check column to dataframe with partition check values
    data_transformed['check_string'] = partition_check_values

    # Adding partition user_list to final_users_edge_list
    final_users_edge_list.append(data_transformed)

# Creating the final dataframe to be written to the edge file
final = pd.concat(final_users_edge_list)
# Dropping the duplicate edges found using the check_string column
final = final.drop_duplicates('check_string')
# Dropping the check_string column as it is not needed in the edge list
final = final.drop(['check_string'], axis = 1)

# Creating file to hold all user connections or edges
with open('Q3.out', 'a') as f:
    if not final.empty:
        edges = final.to_string(header = False, index = False)
        f.write(edges)
# Closing file after writing
f.close()












