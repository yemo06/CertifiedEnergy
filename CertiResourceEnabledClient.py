import json
import requests
import base64
import datetime
from urllib.parse import urlencode
import config

from requests.api import get

client_id = config.clientId
client_secret = config.clientSecret

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id =client_id
        self.client_secret = client_secret

    def get_client_crednetials(self):
        # Returns a base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret

        if client_secret == None or client_id == None:
            raise Exception("You must set client id and client_secret")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_crednetials()
        return  {
        "Authorization" : f"Basic {client_creds_b64} "
        }

    def get_token_data(self):
        return {
        "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()

        r = requests.post(token_url, data=token_data, headers=token_headers)
        
        if r.status_code not in range(200, 299):
            raise Exception ("Did not authenticate client.")
            #return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in =data['expires_in']# seconds
        expires = now  + datetime.timedelta(seconds= expires_in)
        self.access_token =access_token
        self.access_token_expires =expires
        self.access_token_did_expire = expires <now
        return True
        

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires<now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()    
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers


    def get_resource(self, lookup_id,resource_type='albums', version="v1",include_groups='include_groups=album', limit='limit=50', market='market=US'):
        endpoint =f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/albums?{include_groups}&{market}&{limit}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        #print(r.json())
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=4)

        if r.status_code not in range(200, 299):
            r.status_code
            return{}
        return r.json()


    def getAlbumresource(self, lookupId, resourceType='albums', version='v1',market= "market=US" ):
        endpoint =f"https://api.spotify.com/{version}/{resourceType}/{lookupId}?{market}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        #print(r.json())
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=4)

        if r.status_code not in range(200, 299):
            r.status_code
            return{}
        return r.json()
    
    
    def get_album(self, _id ):
        return self.getAlbumresource(_id, resourceType="albums")


    def get_artist(self, _id ):
        
        return self.get_resource(_id, resource_type="artists", limit='limit=49')

    

    def search (self,query, resultlimit, search_type = 'artist'): #type
        access_token = self.get_access_token()
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower(), "limit": resultlimit})
        #print (data)

        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        #print(r.json())
        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(r.json(), f, ensure_ascii=False, indent=4)
        if r.status_code not in range(200, 299):
            return{}
        return r.json()

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
        

# spotify=SpotifyAPI(client_id, client_secret)
# searchResult= spotify.search("Drake", 1, search_type= "artist")
# #print(type(searchResult))
# artistUri =searchResult['artists']['items']

# result =getDictfromList("uri",artistUri)
#print(result)

# for i in range(len(artistUri)):
#     print (artistUri[i])

#print(type(artistUri))
#response1= spotify.get_artist("3TVXtAsR1Inumwj472S9r4")
#print(response1)
