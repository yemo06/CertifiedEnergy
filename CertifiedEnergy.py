import CertiResourceEnabledClient as crec

#getting artist (Drake) uri code 
spotify = crec.SpotifyAPI(crec.client_id,crec.client_secret)
searchResults = spotify.search("Drake",1,search_type="artist")
artistUri = searchResults['artists']['items']#Before the 'getDictfromList' function call the 'uri' String looks like "spotify:artist:3TVXtAsR1Inumwj472S9r4" 
artistUricode= crec.getUriDictfromList("uri",artistUri)#After the 'getDictfromList' function call the 'uri' String looks like "3TVXtAsR1Inumwj472S9r4"

#getting a list of drakes albums
artist= spotify.get_artist(artistUricode)
albumUri = artist['items']
albumUriList =crec.getUriListDictfromList2("uri", albumUri)#.split(":",2)[2] #Returns a list

print(albumUriList) #So it looks were dealing with duplicates at the track level so why not compare duplicte albums b explicit if not pop, else, keep the first
print(len(albumUriList))

#getting the tracks from drakes albums
# trackUrilist =[]
# for i in range(len(albumUriList)):
#     tracks= spotify.get_album(albumUriList[i])
#     trackUri =tracks['tracks']['items']
#     # print(tracks)
#     trackUrilist[i] =crec.getUriListDictfromList2("uri",crec.getGenAttrDictfromList("explicit",trackUri) )#URI codes for all the tracks
#     print(trackUrilist)
#     print (len(trackUrilist))
#     # print(tracks)

#for uricode in albumUriList:
 # with open('filename.txt', 'w') as f:
    #     print(trackUri, file=f)


#print(spotify.get_artist(artistUricode))




