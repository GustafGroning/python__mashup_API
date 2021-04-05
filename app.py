from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)


mashUpDict = {"MBID": "", "description": "", "albums": ""} #dictionary där samtlig data sparas och till slut returneras.

def FindWikipediaURL(IDConvert, URLRework): #hittar via WikiData rätt ID för en sökning på Wikipedia.

    wikiDataURL = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + IDConvert + "&format_=json&props=sitelinks&format=json")
    response = requests.get(wikiDataURL)
    data = response.text 
    parsed = json.loads(data) 

    wikipediaID = parsed['entities'][IDConvert]['sitelinks']['enwiki']['title']
    
    return(GetWikipediaText(wikipediaID.replace(" ", "_"), URLRework))

def GetWikipediaText(wikipediaID, URLRework): #hämtar description text från Wikipedia.

    wikipediaURL = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + wikipediaID + "&formatversion=2&rvprop=content&rvslots=*&prop=extracts"
    response = requests.get(wikipediaURL) 
    data = response.text 
    parsed = json.loads(data) 

    mashUpDict['description'] = (parsed['query']['pages'][0]['extract']) 
    return(GetCoverArt(URLRework))

def GetCoverArt(URLRework):
    gatheredAlbums = {} #dictionary som sparar datan till slutreturningen (mashUpDict)

    response = requests.get(URLRework) 
    data = response.text
    parsed = json.loads(data)

    for entry in parsed['release-groups']:
        
        coverDictionary = {}
        coverTitle = entry['title']
        coverID = entry['id']
        coverUrl = "http://coverartarchive.org/release-group/" + coverID 
        coverResponse = requests.get(coverUrl)

        if coverResponse.status_code == 200: #vissa albums fungerade inte, kanske felaktiga länkar från MusicBrainz. if-satsen fångar dessa 
            #och hoppar över trasiga länkar.
            coverdata = coverResponse.text 
            coverParsed = json.loads(coverdata)

            imageLink = coverParsed['images'][0]['image']

            coverDictionary['image'] = imageLink
            coverDictionary['id'] = coverID
            coverDictionary['title'] = coverTitle

            gatheredAlbums[coverTitle] = coverDictionary #skapar hela albumet.
      
    
    mashUpDict['albums'] = gatheredAlbums
    finalOutput = json.loads(json.dumps(mashUpDict, indent = 4))
    return(finalOutput) #gör om slutlig output till JSON format.
    
@app.route('/')
def intro():
    instructions = "to run the script, go too localhost/search/<>, with your requsted MBID inside < >"
    return(instructions)

@app.route('/search/<MBID>', methods=['GET'])

def StartUp(MBID): #tar ett MBID från användaren och hittar ett ID som skickas vidare till WikiData eller Wikipedia.
    musicBrainzURL = "http://musicbrainz.org/ws/2/artist/" + MBID + "?&f%20mt=json&inc=url-rels+release-groups&fmt=json"
    URLRework = ((musicBrainzURL.replace('<', '').replace('>', '')))
    response = requests.get(URLRework) 

    if response.status_code != 200: #avslutar programmet ifall det inmatade MBID inte är korrekt eller URL på annat sätt inte går igenom.
        errorStatus = str(response.status_code)
        return("invalid MBID, status code: " + errorStatus)

    mashUpDict['MBID'] = (MBID)
    data = response.text 
    parsed = json.loads(data) 

    for entry in parsed['relations']: 
        
        if entry['type'] == 'wikidata':
            IDConvert = entry['url']['resource']
            return(FindWikipediaURL(IDConvert.split("/")[-1], URLRework)) #URLRework skickas med för att kunna hitta cover art senare, som behöver 
            # komma åt samma URL. Sista splitten av IDConver (-1) innehåller ID till Wikidatas API.
            
        elif entry['type'] == 'wikipedia':
            pass
        # Hittade inget ID som länkade direkt till Wikipedia, kunde därför inte testa detta case. 
        # baserat på musicBrainz format bör dock lösningen vara;
        # wikipediaID = entry['title] - som sedan skickas direkt till GetWikipediaText som wikipediaID, utan att gå igenom FindWikipediaURL.
            
# MBID ATT TESTA MED (nirvana) - 5b11f4ce-a62d-471e-81fc-a69a8278c7da

if __name__ == '__main__':
    app.run(debug=True)
