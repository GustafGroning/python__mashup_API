## python__mashup_API


# Intro
A RESTful API that gathers and formats data from 3 separate API’s (MusicBrainz, Wikidata/Wikipedia and Cover Art Archives) about an artist and their releases.

Searches are based on a MBID (identifier from MusicBrainz API), which is used to gather and output:
* ID (from MusicBrainz)
* Description for the artist/band (from Wikipedia)
* All releases from the artist/band with name and link to the front image of the release (from Cover Art Archives).

The output is in a JSON format.

# Installation
The system needs a version of Python3 and the Flask module. Both json and requests (Python3 modules that are required for running the app) are included in any valid installation of Python3 and do not need to be installed independently.

## Start the API
1. open a terminal window in the project folder
2. Enter ```python3 app.py ```
<br> the API is now running on your machine and can be accessed.

The API can be accessed through the command line or any browser that can handle JSON

## browser
1. Enter``` localhost:5000/search/MBID ``` <br> 5000 is the automatic port used by Flask, MBID is the identifier you want to search for 
<br> %3C5b11f4ce-a62d-471e-81fc-a69a8278c7da%3E is a valid MBID for the band Nirvana


## command line
1. Open a terminal window in the project folder
2. Enter ``` curl localhost:5000/search/%3C5b11f4ce-a62d-471e-81fc-a69a8278c7da%3E ``` 



# Testing
The main issue that could occur is if a user inputs an invalid MBID. To avoid this, a case is included at Start up:
```if response.status_code != 200:  ``` <br>
```errorStatus = str(response.status_code) ``` <br>
```return("invalid MBID, status code: " + errorStatus)```
<br>
Besides this, no other user error is possible since the rest of the information is gathered by the API itself.
# Issues
MusicBrainz can link directly from Wikipedia instead of going through WikiData, but I couldn’t find any ID’s linking directly, so I couldn’t test my implementation. Based on the format of MusicBrainz output a hypothetical solution is included in the source codes comments which should work for implementation, but hasn’t been tested properly.
