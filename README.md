# Big Data Analytics Project
Multiple Python programs created for a big data class. The dataset which the analytics were performed on were a subset of Yelp's businesses, reviews, and user data. The dataset can be found and downloaded from Kaggle
https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/versions/3. The first program (descriptive-analytics.py) does descriptive analytics on the dataset. The second program (frequency-distributions.py) computes useful frequency 
distributions from the dataset. The third program (social-network.py) creates a social network of Yelp friends from the above dataset. The fourth and final program (network-analytics.py) performs basic network analytics on the constructed 
social network from the third program.
## Usage
### descriptive-analytics.py
Takes businesses from yelp_academic_dataset_business.json, a two-letter state/province abbreviation ST (case-sensitive), and a name of a city CITY (case-sensitive), and computes and writes the answer to a text file named Q1.out in the current working directory. The file Q1.out consists of six line-separated numbers as follows:

* The number of businesses in the CITY, ST
* The average number of stars of businesses in the CITY, ST
* The number of restaurants in the CITY, ST
* The average number of stars of restaurants in the CITY, ST
* The average number of reviews for all businesses in the CITY, ST
* The average number of reviews for restaurants in the CITY, ST

To run the program:
```
$ python descriptive-analytics.py (path to yelp_academic_dataset_business.json) CITY ST
```
Example:
```
$ python descriptive-analytics.py yelp_academic_dataset_business.json Vancouver BC
```

Sample output (Q1.out):
```
10299
3.6
4275
3.51
41.63
69.26
```

### frequency-distributions.py
Takes businesses from yelp_academic_dataset_business.json, a two-letter state/province abbreviation ST (case-sensitive), and a name of a city CITY (case-sensitive), and performs the following tasks:

1. For all restaurants in the CITY, ST, it will compute the frequency distribution of the number of restaurants in each category of restaurants (e.g., Japanese, Chinese, Canadian, Italian, etc.). The program will only consider restaurant categories that are based on geographical origin. For example, "Mediterranean" is a restaurant category while "Sandwiches" is not. Please note that a restaurant can fall into multiple categories.
The program will write the top-10 categories to a text file named Q2_part1.out in the current working directory. The output will be one line per pair of values as follows:
    ```
    category:#restaurants
    ```
    For example:
    ```
    Japanese:525
    Chinese:425
    Canadian (New):345
    Italian:230
    Vietnamese:216
    American (New):182
    American (Traditional):181
    Asian Fusion:177
    Mediterranean:149
    Indian:144
    ```

2. For all restaurants in the CITY, ST, it will compute the frequency distribution of the number of reviews submitted for each category of restaurants (e.g., Japanese, Chinese, Canadian, Italian, etc.). The program will only consider restaurant categories that are based on geographical origin. For example, "Mediterranean" is a legit restaurant category while "Sandwiches" is not. Please note that a restaurant can fall into multiple categories.
The program will write the top-10 most reviewed categories in descending order (from the most reviewed category to the least reviewed) to a text file named Q2_part2.out in the current working directory. The output will be one line per triplet as follows:
    ```
    category:#reviews:average_review_count
    ```
    For example:
    ```
    Japanese:48181:91.77
    Canadian (New):39046:113.18
    Chinese:21924:51.59
    American (New):21764:119.58
    Italian:19729:85.78
    American (Traditional):17222:95.15
    Vietnamese:13829:64.02
    Asian Fusion:12416:70.15
    Middle Eastern:11849:101.27
    French:11735:126.18
    ```

3. Create a bar chart that shows the top-5 (NOT top-10) restaurant categories identified in part (1), where the x-axis represents the restaurant category, and the y-axis represents its frequency (#restaurants). The size of the bar chart will be 10-inch-by-10-inch. The chart will be properly labeled. Saves the plot as a PDF file named Q2_part3.pdf in the current working directory.

To run the program:
```
$ python frequency-distributions.py (path to yelp_academic_dataset_business.json) CITY ST
```
Example:
```
$ python frequency-distributions.py yelp_academic_dataset_business.json Vancouver BC
```

### social-network.py
The social network that is created will be represented as a graph, where the vertices represent the Yelp users and the edges represent the friendships between Yelp users.
The graph/network will be represented in a file using the edge list format. An edge list is a list that represents all the edges in a graph. Each edge is represented as a space-separated pair of vertices. For example, a small fully connected triangle-like graph between vertices c1, c2, c3 would be represented in the edge list as:
```
c1 c2
c2 c3
c3 c1
```
Note that the order of the lines does not matter, and edges are bidirectional (so either "c1 c2" or "c2 c1" should be listed but NOT both).

Takes users from yelp_academic_dataset_user.json and an integer n (n >= 100), that creates the social network of Yelp friends among Yelp users who sent no less than n useful votes, and writes the edge list of the created graph to a text file named Q3.out in the current working directory. Will only consider Yelp users who sent no less than n useful votes. For example, users c1 and c2 are friends, who sent n+1 and n-1 useful votes, respectively. In this case, neither "c1 c2" nor "c2 c1" will be listed.

To run the program:
```
$ python social-network.py (path to yelp_academic_dataset_user.json) n
```
Example (the following command will create the social network of Yelp friends among Yelp users who sent no less than 100 useful votes):
```
$ python social-network.py yelp_academic_dataset_user.json 100
```

### network-analytics.py
Takes a Yelp social network as an edge list in a text file (the format is the same as the output from social-network.py), and computes the following network statistics and writes the answer to a text file named Q4.out in the current working directory.

* the number of vertices (|V|) and the number of edges (|E|) of the network. The output should be two space-separated integers.
* The average node degree of the graph (avgNodeDegree). The degree of a node is the number of edges that are incident to the node (i.e., #neighbors).
* The number of connected components in the network (#components). A connected component is a connected subgraph that is not part of any larger connected subgraph. The connected components of any graph partition its vertices into disjoint sets, and are the induced subgraphs of those sets. A graph that is itself connected has exactly one component, consisting of the whole graph.
* The number of triangles in the network (#triangles). For example, vertices a1, a2, a3 (the order doesn't matter) form a triangle in the social network if a1 and a2 are friends, a1 and a3 are friends, and a2 and a3 are friends.

The output of (Q4.out) will look like:
```
|V| |E|
avgNodeDegree
#components
#triangles
```
For example:
```
34713 25387
1.46
9327
11571
```

To run the program:
```
$ python network-analytics.py (path to edge list text file)
```
Example:
```
$ python network-analytics.py Q3.out
```
