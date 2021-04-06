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
<br> %3C5b11f4ce-a62d-471e-81fc-a69a8278c7da%3E is a valid MBID for the band Nirvana


## command line
1. Open a terminal window in the project folder
2. Enter ``` curl localhost:5000/search/%3C5b11f4ce-a62d-471e-81fc-a69a8278c7da%3E ``` 



# Testing


A similair case exists for skipping broken links to albums from Cover Art Archive.

Besides this, no other user error is possible since the rest of the information is gathered by the API itself.
# Issues
MusicBrainz can link directly from Wikipedia instead of going through WikiData, but I couldn’t find any ID’s linking directly, so I couldn’t test my implementation. Based on the format of MusicBrainz data a hypothetical solution is included in the source code comments which should work for implementation, but hasn’t been tested properly.
