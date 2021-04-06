import json

mashUpDict = {"MBID": "", "description": "", "albums": {} } 
gatheredAlbums = {}
coverDictionary = {}
x = 0
while x < 5:
    coverDictionary['title'] = "Bleach"
    coverDictionary['id'] = "123"
    coverDictionary['image'] = ".jpg"

    gatheredAlbums[x] = coverDictionary
    x = (x + 1)

mashUpDict['albums'] = gatheredAlbums
print(gatheredAlbums)
print(mashUpDict)
#print(mashUpDict)
#finalOutput = json.loads(json.dumps(mashUpDict, indent = 4))
#print(finalOutput)
