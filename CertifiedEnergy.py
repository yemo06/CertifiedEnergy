from ctypes.wintypes import PINT
import CertiResourceEnabledClient as crec
spotify = crec.SpotifyAPI(crec.client_id,crec.client_secret)

# def Extract(lst,ndx):
#     return [item[ndx] for item in lst]


def getGenAttrDictfromList(key, List):
    returnList =[]
    for diction in List:
        if key in diction:
            returnList.append(diction[key])
    return returnList

def getUriDictfromList(key, List):
    for diction in List:
        if key in diction:
            return diction[key].split(":",2)[2] #to get to the code split on the ":" and grab the 3rd element in the new split string

def getUriListDictfromList2(key, List):
    returnList =[]
    for diction in List:
        if key in diction:
            returnList.append(diction[key].split(":",2)[2])
    return returnList


def getArtist(artist):
    artistSearchResults =spotify.search(artist,1,search_type="artist")
    artistUri =artistSearchResults['artists']['items']
    artistUricode = getUriDictfromList("uri", artistUri)
    return artistUricode

def getArtistAlbums(artistUriCode):
    artist = spotify.get_artist(artistUriCode)
    albumUri = artist['items']
    albumUriList =getUriListDictfromList2("uri", albumUri)
    return albumUriList

def getAlbumInfo(artistAlbumUriList):
    albumInfo =[]
    for album in range(len(artistAlbumUriList)):
        singleAlbum = spotify.get_album(artistAlbumUriList[album])
        albumName= singleAlbum['name']
        albumTracklen= singleAlbum['total_tracks']
        # newList=singleAlbum['tracks']['items']
        explicitCount =getGenAttrDictfromList('explicit',singleAlbum['tracks']['items']).count(True)
        albumInfo.append([albumName,albumTracklen,explicitCount,artistAlbumUriList[album]])
    return albumInfo

### Here is where the algorithm for filtering Non-Explicit albums should go ###
def getExplicitAlbums(albumInfoList):
    explicitList = []
    l = 1
    for r in range(1,len(albumInfoList)):
        if albumInfoList[r][0] != albumInfoList[r-1][0] :
            albumInfoList[l] =albumInfoList[r]
            l+=1
        else:
            if((albumInfoList[r][1] >= albumInfoList[r-1][1]) & (albumInfoList[r][2] >= albumInfoList[r-1][2] )):
                albumInfoList[l] =albumInfoList[r]
                l+=1
            # else:
            #     continue #Sorts most of the non-explicit/dupl icate albums, have to figure out this last else case to make sure mutiple cases that have the same alnum dont stick around, maybe turn the else into an else if

        
            
    # for album in range(len(albumInfoList)):
    #     if album[0] in explicitList:
    #         fromEList = explicitList[explicitList.index(album[0])] # "fromElist refrences the an album & albumdata in the explicitList based the album were serching for
            
    #         if (album[1] >= fromEList[1]) & (album[2] >= fromEList[2]): #if the track list & the amount of explcit songs in one album is greater than or equal to another
    #             explicitList.pop(explicitList.index(album[0]))
    #             explicitList.append(album)
        
    #     else:
    #         explicitList.append(album)
            
            
                
                 
             
        # if albumInfoList[album][2] > 0:
        #     explicitList.append(albumInfoList[album])
    return albumInfoList[:l]
#getting artist (Drake) uri code 

def getTrackCodeName (albumList):
    ### Algorithm to get the uri of tracks
    ### Creates a new List called trackNamexCodes which will be filled with track names & id codes
    ### The for loops goal is to is to create list that contains a sublists of track names, and track identifer codes codes.
    ### This happens by getting the name and then the corresponding uri code and zipping them together, then appending the lists together.
    
    trackNamexCodes = []
    
    for x in range(len(albumList)):
        trackListuri = spotify.get_album(albumList[x][3])['tracks']['items'] # gets the dict with uri
        trackListuris =crec.getUriListDictfromList2('uri',trackListuri)
        trackListnames = crec.getGenAttrDictfromList('name',trackListuri)
        trackNamexCodes.append(list(zip(trackListnames,trackListuris)))#gets a list of uri's and track names for each ablum    
    return trackNamexCodes

def getTrackEnergy(tracksList):
    trackEnergyList =[]
    for x in range(len(tracksList)):
        for y in range(len(tracksList[x])):
        # Working on algorithm to get energy of songs from track analysis
            trackEnergyList.append([tracksList[x][y][0],spotify.get_trackenergy(tracksList[x][y][1])['energy']]) 
    return trackEnergyList


# searchResults = spotify.search("Drake",1,search_type="artist")
# artistUri = searchResults['artists']['items']#Before the 'getDictfromList' function call the 'uri' String looks like "spotify:artist:3TVXtAsR1Inumwj472S9r4" 
# artistUricode= crec.getUriDictfromList("uri",artistUri)#After the 'getDictfromList' function call the 'uri' String looks like "3TVXtAsR1Inumwj472S9r4"




#getting a list of drakes albums

# artist= spotify.get_artist()
# albumUri = artist['items']
# albumUriList =crec.getUriListDictfromList2("uri", albumUri)#.split(":",2)[2] #Returns a list

artistUriCode = getArtist("Drake")

artistAlbumUriList = getArtistAlbums(artistUriCode)
    
albumInfoList =getAlbumInfo(artistAlbumUriList)
# print(albumInfoList[0])

explicitList =getExplicitAlbums(albumInfoList)
print(explicitList)
print(len(explicitList))

# trackNamesxCodes =getTrackCodeName(explicitList)

# trackEnergyList = getTrackEnergy(trackNamesxCodes)

# print((trackEnergyList))
# print(len(trackEnergyList))
# print(albumInfoList)


# TODO
# Next is setting up algorithm to disect and arrange data by album,
## Finishing a way to better the time complexity of the algorithm
# Writing some tests / figuring out how to test
# Rank the top 5 songs ineach album 
# Rank albums total energy by average, 


# print(albumUriList) #So it looks were dealing with duplicates at the track level so why not compare duplicte albums b explicit if not pop, else, keep the first
# print(len(albumUriList))

#GetExplcit Albums only


    





### Work on refactring this next ###

# print(tracksList)
# print(len(tracksList))


# test1 = spotify.get_trackenergy(tracksList[0][1][1])['energy'] # Working on algorithm to get energy of songs from track analysis
# print(type(test1))
# print(tracksList[0][1][0] + " Energy "+ str(test1))










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




