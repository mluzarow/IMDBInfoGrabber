#region Dependencies
import httplib
import logging
import os
import re
import urllib2
import time
#endregion Dependencies

#region Defines
END_ID = 5000
START_ID = 1
#endregion Defines

################################################################################
## anime.py
##
## Console application will take very anime arguments and recommend up to 3
## very anime recommendations. Uses ANN API.
################################################################################

def writeHistory (movies):
    pathFile = 'IDs/Movies.txt'

    # Check if the directiory exists
    if (not os.path.exists ('IDs')):
        # It does not exist, so create it
        os.makedirs ('IDs')

    # Check if the file exists
    if (not os.path.isfile (pathFile)):
        # File does not exist, so make it
        with open (pathFile, 'w') as f:
            f.write ('0')
        f.closed

    # Open History and write all the values in there (overwriting everything)
    with open (pathFile, 'w') as f:
        for id, rating in movies.items():
            f.write (str(id) + ":" + str(rating) + '\n')
    f.closed

def dictionarise(input):
    j = dict()

    pairs = input.split("\",\"")
    for pair in pairs:
        pair = re.sub ('\"', "", pair)
        pair = re.sub ('{', "", pair)
        pair = re.sub ('}', "", pair)

        dpair = pair.split(':')

        j[dpair[0]] = dpair[1]
    return j

def getRating(currentID):
    # Set up OMDB path for the ID
    path = "http://www.omdbapi.com/?i=tt%07d&plot=short&r=json" % currentID
    try:
        # Follow URL
        response = urllib2.urlopen(path)
        # Get data
        j = response.read()

        dj = dictionarise(j)

        return float(dj["imdbRating"])

    except urllib2.HTTPError, e:
        logging.warning('HTTPError=%s, animeId=%s' % (str(e.code), str(currentID)))
    except urllib2.URLError, e:
        logging.warning('URLError=%s, animeId=%s' % (str(e.reason), str(currentID)))
    except httplib.HTTPException, e:
        logging.warning('HTTPException, animeId=%s' % str(currentID))
    except Exception:
        return None
        import traceback
        logging.warning('generic exception: ' + traceback.format_exc())

############################ MAIN IS RIGHT HERE ################################
#region Main

# Dict of all ID : ratings
movies = dict()
# Current movie ID
currentID = START_ID
# Error code
error = 0
print ("\n===Beginning Search===")

# Run program while ID is still valid
while not error:
    buff = getRating(currentID)

    if buff == None:
        print "[%07d] has no imdbRating." % currentID
        currentID += 1
    else:
        movies[currentID] = buff
        print "Recieved: [%07d] R: %.2f" % (currentID, buff)
        currentID += 1

    time.sleep(3)
    if currentID == END_ID:
        error = 1
        print "Reached the end ID."

print "Writing"
writeHistory(movies)
print "Done"
#endregion Main
