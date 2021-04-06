## python__mashup_API

# Intro
A RESTful API that gathers and formats data from 3 separate API’s (MusicBrainz, Wikidata/Wikipedia and Cover Art Archives) about an artist and their releases.

Searches are based on a MBID (identifier from MusicBrainz API), which is used to gather and output:
* ID (from MusicBrainz)
* Description for the artist/band (from Wikipedia)
* All releases from the artist/band with name and link to the front image of the release (from Cover Art Archives).

The output is in a JSON format.

# Installation
The system needs a version of Python3, requests and the Flask module. 

## Start the API
1. open a terminal window in the project folder
2. Enter ```python3 app.py ```
<br> the API is now running on your machine and can be accessed.

The API can be accessed through the command line or any browser that can handle JSON

## browser
1. Enter``` localhost:5000/search/MBID ``` <br> 5000 is the automatic port used by Flask, MBID is the identifier you want to search for 
<br> 5b11f4ce-a62d-471e-81fc-a69a8278c7da is a valid MBID for the band Nirvana


## command line
1. Open a terminal window in the project folder
2. Enter ``` curl localhost:5000/search/5b11f4ce-a62d-471e-81fc-a69a8278c7da ``` 



# Testing
A unittest is performed by checking if the first album title of the inputed MBID (Nirvana) is the correct name (should be Bleach). Since Nirvana doesn't publish anymore albums, the test should always succeed as long as a new commit hasn't broken the code base or one of the relevant APIs are down. <br>
to test this, start the API as shown above, then open a terminal in your project folder and input ``` python3 app_test.py ```

# Issues
MusicBrainz can link directly from Wikipedia instead of going through WikiData, but I couldn’t find any ID’s linking directly, so I couldn’t test my implementation. Based on the format of MusicBrainz data a hypothetical solution is included in the source code comments which should work for implementation, but hasn’t been tested properly.
