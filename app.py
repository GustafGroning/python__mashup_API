from flask import Flask, jsonify
import requests
import json


app = Flask(__name__)


mashUpDict = {"MBID": "", "description": "", "albums": ""} 
#TODO: är alla variabler namngedda korrekt?

def findWikipediaURL(IDConvert, urlRework):

    wikiDataURL = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + IDConvert + "&format_=json&props=sitelinks&format=json")
    response = requests.get(wikiDataURL)
    data = response.text 
    parsed = json.loads(data) 

    wiki_ID = parsed['entities'][IDConvert]['sitelinks']['enwiki']['title']
    
    return(GetWikipediaText(wiki_ID.replace(" ", "_"), urlRework))

def GetWikipediaText(wiki_ID, urlRework):

    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" + wiki_ID + "&formatversion=2&rvprop=content&rvslots=*&prop=extracts"
    
    response = requests.get(url) #hämter hela api:t

    data = response.text #gör om responsen till ett läsbart format

    parsed = json.loads(data) # gör om json string till ett objekt

    #print(parsed['query']['pages'][0]['extract'][0:1000]) 
    mashUpDict['description'] = (parsed['query']['pages'][0]['extract'][0:1000]) #det ska inte ligga någon 0:1000 slice i slutversionen, men det gör det lättare att läsa output just nu.

    #return(mashUpDict)

    return(GetCoverArt(urlRework))

def GetCoverArt(brainUrl):
    gatheredAlbums = {}
    
    response = requests.get(brainUrl) #just nu bärs brainUrl genom hela grejen, det är inte en snygg lösning. Finns det någon bättre?
    #coverUrl = "http://ia803208.us.archive.org/11/items/mbid-" + a146429a-cedc-3ab0-9e41-1aaf5f6cdc2d + "/index.json"
    
    data = response.text
    parsed = json.loads(data)

    for entry in parsed['release-groups']:
        
        coverDictionary = {}
        coverTitle = entry['title']
        coverID = entry['id']
        coverUrl = "http://coverartarchive.org/release-group/" + coverID 
        # coverartarchive.org/release-group/810068af-2b3c-3e9c-b2ab-68a3f3e3787d det här formatet vill vi ha
        coverResponse = requests.get(coverUrl)

        if coverResponse.status_code == 200:
            coverdata = coverResponse.text 
            coverParsed = json.loads(coverdata)

            imageLink = coverParsed['images'][0]['image']

            
            
            coverDictionary['image'] = imageLink
            coverDictionary['id'] = coverID
            coverDictionary['title'] = coverTitle
            gatheredAlbums[coverTitle] = coverDictionary
      
    
    mashUpDict['albums'] = gatheredAlbums
    finalOutput = json.loads(json.dumps(mashUpDict, indent = 4))
    return(finalOutput)
    



@app.route('/')
def hi():
    return("hello user!")

@app.route('/search/<MBID>', methods=['GET'])

def startUp(MBID): #tar ett MBID från användaren och hittar ett ID som skickas vidare till WikiData eller Wikipedia.
# MBID ATT TESTA MED (nirvana) - 5b11f4ce-a62d-471e-81fc-a69a8278c7da
    musicBrainzURL = "http://musicbrainz.org/ws/2/artist/" + MBID + "?&f%20mt=json&inc=url-rels+release-groups&fmt=json"
    urlRework = ((musicBrainzURL.replace('<', '').replace('>', '')))
    response = requests.get(urlRework) 

    if response.status_code != 200:
        status = str(response.status_code)
        return("invalid MBID, status code: " + status)


    mashUpDict['MBID'] = (MBID)
    
    data = response.text 
    parsed = json.loads(data) 

    for entry in parsed['relations']: 
        
        if entry['type'] == 'wikidata':
            IDConvert = entry['url']['resource']
            return(findWikipediaURL(IDConvert.split("/")[-1], urlRework)) #urlRework skickas med för att kunna hitta cover art senare.
            
        elif entry['type'] == 'wikipedia':
            pass
        # Hittade inget ID som länkade direkt till Wikipedia, kunde därför inte testa detta case. 
        # baserat på musicBrainz format bör lösningen dock vara;
        # Wiki_ID = entry['title] - som sedan skickas direkt till GetWikipediaText.
            


if __name__ == '__main__':
    app.run(debug=True)
