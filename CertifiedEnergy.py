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


# explcitAlbumlist = []
# index= 0
# # for index in range(len(albumInfolist)-1):
# while(index< len(albumInfolist)-1):
#     while (albumInfolist[index][0] == albumInfolist[index+1][0]):
#         if(albumInfolist[index][1] == albumInfolist[index+1][1] and albumInfolist[index][2] == albumInfolist[index+1][2]):
#             explcitAlbumlist.append(albumInfolist[index])
#             index+=1
#             break
#         else:
#             if(albumInfolist[index][2] > albumInfolist[index+1][2]):
#                 explcitAlbumlist.append(albumInfolist[index])
#                 index+=1
#                 break
#             elif(albumInfolist[index][1] > albumInfolist[index+1][1]):
#                 explcitAlbumlist.append(albumInfolist[index])
#                 index+=1
#                 break
#             else:
#                 explcitAlbumlist.append(albumInfolist[index+1])
                
#     index+=1
    
#     print(explcitAlbumlist)


    
            



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




