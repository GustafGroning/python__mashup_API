## python__mashup_API


# Intro
A RESTful API that gathers and formats data from 3 separate API’s (MusicBrainz, Wikidata/Wikipedia and Cover Art Archives) about an artist and their releases.

Searches are based on a MBID (identifier from MusicBrainz API), which is used to gather and output:
* ID (from MusicBrainz)
* Description for the artist/band (from Wikipedia)
* All releases from the artist/band with name and link to the front of the release (from Cover Art Archives).

The output is in a JSON format.

# Installation


# Testing

# Issues
MusicBrainz can link directly from Wikipedia instead of going through WikiData, but I couldn’t find any ID’s linking directly, so I couldn’t test my implementation. Based on the format of MusicBrainz output a hypothetical solution is included in the source codes comments which should work for implementation, but hasn’t been tested properly.
