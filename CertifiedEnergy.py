import CertiResourceEnabledClient as crec
from collections import Counter

def Extract(lst,ndx):
    return [item[ndx] for item in lst]


#getting artist (Drake) uri code 
spotify = crec.SpotifyAPI(crec.client_id,crec.client_secret)
searchResults = spotify.search("Drake",1,search_type="artist")
artistUri = searchResults['artists']['items']#Before the 'getDictfromList' function call the 'uri' String looks like "spotify:artist:3TVXtAsR1Inumwj472S9r4" 
artistUricode= crec.getUriDictfromList("uri",artistUri)#After the 'getDictfromList' function call the 'uri' String looks like "3TVXtAsR1Inumwj472S9r4"

#getting a list of drakes albums
artist= spotify.get_artist(artistUricode)
albumUri = artist['items']
albumUriList =crec.getUriListDictfromList2("uri", albumUri)#.split(":",2)[2] #Returns a list

# print(albumUriList) #So it looks were dealing with duplicates at the track level so why not compare duplicte albums b explicit if not pop, else, keep the first
# print(len(albumUriList))

#GetExplcit Albums only
albumInfolist = []
for album in range(len(albumUriList)):
    singleAlbum = spotify.get_album(albumUriList[album])
    albumName= singleAlbum['name']
    albumTracklen= singleAlbum['total_tracks']
    newList=singleAlbum['tracks']['items']
    explicitCount =crec.getGenAttrDictfromList('explicit',newList).count(True)
    albumInfolist.append([albumName,albumTracklen,explicitCount,albumUriList[album]])


### Here is where the algotithem for filtering Non-Explicit albums should go ###
explicitList = []
for album in range(len(albumInfolist)):
    if albumInfolist[album][2] > 0:
        explicitList.append(albumInfolist[album])
        # album+=1
    # print((explicitList))

### Algorithm to get the uri of tracks
Tracklistcodes = []
for x in range(len(explicitList)):

        trackListuri = spotify.get_album(explicitList[x][3])['tracks']['items'] # gets the dict with uri
        trackListuris =crec.getUriListDictfromList2('uri',trackListuri)
        trackListnames = crec.getGenAttrDictfromList('name',trackListuri)
        Tracklistcodes.append(list(zip(trackListnames,trackListuris)))#gets a list of uri's and track names for each ablum

# print(Tracklistcodes)
# print(len(Tracklistcodes))

test1 = spotify.get_trackenergy(Tracklistcodes[0][1][1])['energy'] # Working on algorithm to get energy of songs from track analysis
print(type(test1))
# test2 = crec.getGenAttrDictfromList('energy',test1)
print(Tracklistcodes[0][1][0] + " Energy "+ str(test1))


# for x in range(len(Tracklistcodes)):

#     trackEnergyList = spotify.get_trackenergy(explicitList[x][1])   
# print(len(Tracklistcodes))
# print(Tracklistcodes)
# print(len(Tracklistcodes))







# uniqueAlbumcount = (Counter(alb[0] for alb in albumInfolist))
# count= Extract(albumInfolist,0)
# # for 
# print (count)

# explcitAlbumlist = [] # Prints every single album, have to rework jdx, specifically to only get the name count.
# idx= 0
# # # # # # for idxin range(len(albumInfolist)-1):
# # # # while(idx< len(albumInfolist)-1):
# # # #     while (albumInfolist[idx][0] == albumInfolist[idx+1][0]):
# for idx in range(len(albumInfolist)-1):
#     if(albumInfolist[idx][0] == albumInfolist[idx+1][0]):
#         for jdx in range(sum(x.count(albumInfolist[idx][0]) for x in albumInfolist)):
        
#             if(albumInfolist[idx][1] == albumInfolist[idx+jdx+1][1] and albumInfolist[idx][2] == albumInfolist[idx+jdx+1][2]):
#                 explcitAlbumlist.append(albumInfolist[idx])
#             else:
#                 if(albumInfolist[idx][2] > albumInfolist[idx+jdx+1][2]):
#                     explcitAlbumlist.append(albumInfolist[idx])

#                 elif(albumInfolist[idx][1] > albumInfolist[idx+jdx+1][1]):
#                     explcitAlbumlist.append(albumInfolist[idx])
                    
#                 else:
#                     explcitAlbumlist.append(albumInfolist[idx+jdx+1])
                
               
# # print(albumInfolist[0].count(albumInfolist[0][0]))
# # print(sum(x.count(albumInfolist[19][0]) for x in albumInfolist))
# print(explcitAlbumlist)
# print(len(explcitAlbumlist))

    
            



# print(explcitAlbumlist)# Puts all the general info needed to make a formula to get rid of Non-Explicit alnums Next is the generalzation and the f
# print(len(explcitAlbumlist))

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




