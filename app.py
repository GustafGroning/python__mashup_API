from flask import Flask, jsonify
import requests
import json


app = Flask(__name__)


mashUpDict = {} 


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

    #print(parsed['query']['pages'][0]['extract'][0:1000]) #det ska inte ligga någon 0:1000 slice i slutversionen, men det gör det lättare att läsa output just nu.
    mashUpDict['description'] = (parsed['query']['pages'][0]['extract'][0:1000])

    return(mashUpDict)

    #return(GetCoverArt(urlRework))


@app.route('/')
def hi():
    return("hello user!")

@app.route('/search/<MBID>', methods=['GET'])

# --------------------------------------
# TA INTE BORT STARTUP DEN FUNKAR BRA!!!
# --------------------------------------
def startUp(MBID): #tar ett MBID från användaren och hittar ett ID som skickas vidare till WikiData eller Wikipedia
# MBID ATT TESTA MED (nirvana) - 5b11f4ce-a62d-471e-81fc-a69a8278c7da
    musicBrainzURL = "http://musicbrainz.org/ws/2/artist/" + MBID + "?&f%20mt=json&inc=url-rels+release-groups&fmt=json"
    urlRework = ((musicBrainzURL.replace('<', '').replace('>', '')))
    response = requests.get(urlRework) 

    mashUpDict['MBID'] = ((musicBrainzURL.replace('<', '').replace('>', '')))
    
    data = response.text 
    parsed = json.loads(data) 

    for entry in parsed['relations']: 
        
        if entry['type'] == 'wikidata':
            IDConvert = entry['url']['resource']
            return(findWikipediaURL(IDConvert.split("/")[-1], urlRework)) #urlRework skickas med för att kunna hitta cover art senare.
            
        elif entry['type'] == 'wikipedia': #den här måste göras klart
            pass #TODO: hur funkar det om man ska hitta wikipedia? Hitta ett exempel MBID som leder direkt till Wikipedia för test.
            


if __name__ == '__main__':
    app.run(debug=True)
