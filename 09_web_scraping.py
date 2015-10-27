'''
CLASS: Web Scraping with Beautiful Soup

What is web scraping?
- Extracting information from websites (simulates a human copying and pasting)
- Based on finding patterns in website code (usually HTML)

What are best practices for web scraping?
- Scraping too many pages too fast can get your IP address blocked
- Pay attention to the robots exclusion standard (robots.txt)
- Let's look at http://www.imdb.com/robots.txt

What is HTML?
- Code interpreted by a web browser to produce ("render") a web page
- Let's look at example.html
- Tags are opened and closed
- Tags have optional attributes

How to view HTML code:
- To view the entire page: "View Source" or "View Page Source" or "Show Page Source"
- To view a specific part: "Inspect Element"
- Safari users: Safari menu, Preferences, Advanced, Show Develop menu in menu bar
- Let's inspect example.html
'''

# read the HTML code for a web page and save as a string
import requests
url = r'https://raw.githubusercontent.com/ga-students/DAT-DC-9/master/data/example.html?token=AG8aPhA-GT-gTGX3iXysiHnk2BLKJmttks5WLS2rwA%3D%3D'
r = requests.get(url)
# 404 error is a user error, or a 500 errors are server type errors
#if you print 'r' you will see its successful.  If you type r.text you get the html
r.text
# convert HTML into a structured Soup object.  Formats the text more cohesively
from bs4 import BeautifulSoup
b = BeautifulSoup(r.text)

# print out the object
print b
print b.prettify() #Adds indentation/ hierarchy of code

# 'find' method returns the first matching Tag (and everything inside of it)
#When you give a name its giving that of the tag
b.find(name='title')
# Tags allow you to access the 'inside text'
b.find(name='title').text
# Tags also allow you to access their attributes.  You need to use brackets to pick out
b.find(name='h1')['id']
# 'find_all' method is useful for finding all matching Tags.  Outputs a result set vs a list.
results=b.find_all(name='p')
type (results)
# ResultSets can be sliced like lists
results[0]
# iterate over a ResultSet
for result in results:
    print result, '\n'
# limit search by Tag attribute
b.find(name="p", attrs={'id':'scraping', 'class':'topic'})
# limit search to specific sections

'''
EXERCISE ONE
'''

# find the 'h2' tag and then print its text
task1 = b.find(name='h2')
print task1

# find the 'p' tag with an 'id' value of 'reproducibility' and then print its text
task2 = b.find(name='p', attrs={'id':'reproducibility'})
print task2

# find the first 'p' tag and then print the value of the 'id' attribute

task3 = b.find(name='p')
print task3
task3b= b.find(name='p')['id']
print task3b
# print the text of all four li tags
task4 = b.find_all(name='li')
print task4

for result in task4:
    print result.text, '\n'
# print the text of only the API resources
task4[0:2]

results = b.find(name='ul', attrs={'id':'api'}).find_all(name='li')
results_next = b.find_all(name='li')
for result in results:
    print result.text
for result in results_next:
    print result.text
'''
Scraping the IMDb website
'''

# get the HTML from the Shawshank Redemption page
r = requests.get('http://www.imdb.com/title/tt0111161/')

# convert HTML into Soup
b = BeautifulSoup(r.text)
print b

# run this code if you have encoding errors
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# get the title
b.find(name='span', attrs= {'class':'itemprop'}).text
# get the star rating (as a float)
rating = b.find(name='div', attrs={'class':'titlePageSprite star-box-giga-star'}).text
float(rating)

'''
EXERCISE TWO
'''

# get the description
description = b.find(name='p', attrs={'itemprop':'description'}).text.strip()
print description
# get the content rating
crating = b.find(name='div', attrs={'class':'infobar'})
crating2 = b.find(name='meta', attrs={'itemprop':'contentRating'})['content']#, 'meta content':'R'})
print crating2
# get the duration in minutes (as an integer)
dur = int(b.find(name='time', attrs={'itemprop':'duration'})['datetime'][2:-1])
dur
'''
OPTIONAL WEB SCRAPING HOMEWORK

First, define a function that accepts an IMDb ID and returns a dictionary of
movie information: title, star_rating, description, content_rating, duration.
The function should gather this information by scraping the IMDb website, not
by calling the OMDb API. (This is really just a wrapper of the web scraping
code we wrote above.)

For example, get_movie_info('tt0111161') should return:

{'content_rating': 'R',
 'description': u'Two imprisoned men bond over a number of years...',
 'duration': 142,
 'star_rating': 9.3,
 'title': u'The Shawshank Redemption'}

Then, open the file imdb_ids.txt using Python, and write a for loop that builds
a list in which each element is a dictionary of movie information.

Finally, convert that list into a DataFrame.
'''

# define a function that accepts an IMDb ID and returns a dictionary of movie information
def get_movie_info(imdb_id):
    r = requests.get('http://www.imdb.com/title/' + imdb_id + '/')
    b = BeautifulSoup(r.text)
    info = {}
    info['title'] = b.find(name='span', attrs={'class':'itemprop', 'itemprop':'name'}).text
    info['star_rating'] = float(b.find(name='span', attrs={'itemprop':'ratingValue'}).text)
    info['description'] = b.find(name='p', attrs={'itemprop':'description'}).text.strip()
    info['content_rating'] = b.find(name='meta', attrs={'itemprop':'contentRating'})['content']
    info['duration'] = int(b.find(name='time', attrs={'itemprop':'duration'}).text.strip()[:-4])
    return info

# test the function
get_movie_info('tt0111161')

# open the file of IDs (one ID per row), and store the IDs in a list

with open('imdb_ids.txt', 'rU') as f:
    ids = []
    for row in f:
        ids.append(row.strip()) 
type(ids)

# get the information for each movie, and store the results in a list

results = []
for id in ids:
    results.append(get_movie_info(id))
    

# check that the list of IDs and list of movies are the same length
len(ids)
len(results)


# convert the list of movies into a DataFrame

import pandas as pd
movielist = pd.DataFrame(results, index=ids)
'''
Another IMDb example: Getting the genres
'''

# read the Shawshank Redemption page again
r = requests.get('http://www.imdb.com/title/tt0111161/')
b = BeautifulSoup(r.text)
print b

# only gets the first genre
fgenre = b.find(name='span', attrs={'class':'itemprop', 'itemprop':'genre'}).text
# gets all of the genres
genres = b.find_all(name='span', attrs={'class':'itemprop', 'itemprop':'genre'})
for genre in genres:
    print genre.text
# stores the genres in a list
genre_list = []
for genre in genres:
    genre_list.append(genre.text)

'''
Another IMDb example: Getting the writers
'''

# attempt to get the list of writers (too many results)
writers = b.find_all(name='span', attrs={'class':'itemprop', 'itemprop':'name'})
# limit search to a smaller section to only get the writers
writers2 = b.find(name='div', attrs={'itemprop':'creator'}).find_all(name='span', attrs={'itemprop':'name'})

'''
Another IMDb example: Getting the URLs of cast images
'''

# find the images by size
images = b.find_all(name='img', attrs={'height':'44', 'width':'32'})
# check that the number of results matches the number of cast images on the page
len(images) #Equals 15, the same number that is on the page
# iterate over the results to get all URLs
for image in images:
    print image['loadlate']



'''
Useful to know: Alternative Beautiful Soup syntax
'''

# read the example web page again
url = r'https://raw.githubusercontent.com/ga-students/DAT-DC-9/master/data/example.html?token=AG8aPhA-GT-gTGX3iXysiHnk2BLKJmttks5WLS2rwA%3D%3D'
r = requests.get(url)

# convert to Soup
b = BeautifulSoup(r.text)

# these are equivalent
b.find(name='p')    # normal way
b.find('p')         # 'name' is the first argument
b.p                 # can also be accessed as an attribute of the object

# these are equivalent
b.find(name='p', attrs={'id':'scraping'})   # normal way
b.find('p', {'id':'scraping'})              # 'name' and 'attrs' are the first two arguments
b.find('p', id='scraping')                  # can write the attributes as arguments

# these are equivalent
b.find(name='p', attrs={'class':'topic'})   # normal way
b.find('p', class_='topic')                 # 'class' is special, so it needs a trailing underscore
b.find('p', 'topic')                        # if you don't name it, it's assumed to be the class

# these are equivalent
b.find_all(name='p')    # normal way
b.findAll(name='p')     # old function name from Beautiful Soup 3
b('p')                  # if you don't name the method, it's assumed to be find_all