import hashlib 
import hmac
import urllib2
import simplejson

KEY = '' #fill in with your key
SECRET = '' #fill in with your secret
API_URL = 'https://api.grooveshark.com/ws3.php?sig='
SESSION_ID = ''
country = {'ID': 221, 'CC1': 0, 'CC2': 0, 'CC3': 0, 'CC4': 0, 'DMA': 0, 'IPR': 0}

def signature(data):
    sig = hmac.new(SECRET, data)
    return sig.hexdigest()

def user_token(username, password):
    token = hashlib.md5(username.lower() + hashlib.md5(password).hexdigest())
    return token.hexdigest()

def api_call(method, parameters={}):
    data = {}
    data['method'] = method
    data['parameters'] = parameters
    data['header'] = {'wsKey': KEY}
    if method != 'startSession':
        data['header']['sessionID'] = SESSION_ID
    
    data_str = simplejson.dumps(data)
    sig = signature(data_str)
    req = urllib2.Request(API_URL+sig, data_str)
    response = urllib2.urlopen(req).read()
    
    return simplejson.loads(response)
    
        
def init(key='', secret=''):
    ''' Create session'''
    if key and secret:
        global KEY
        global SECRET
        KEY = key
        SECRET = secret
    response = api_call('startSession')    
    if response['result']['success'] == True:
        global SESSION_ID
        SESSION_ID = response['result']['sessionID']
    else:
        raise APIError(simplejson.dumps(response['errors']))
        

def authenticate_user(username, password):
    if SESSION_ID == '':
        raise Exception("You need to create a session before you authenticate that session with a username and password")
    else:
        token = user_token(username, password)
        response = api_call('authenticateUser', {'username': username.lower(), 'token': token})
        return response

def get_song_search_results(query, limit=10):
    ''' Perform a song search '''
    results = api_call('getSongSearchResults', {'query': query, 'country':country, 'limit': limit})
    return results

def get_stream_key_stream_server(songID):
    ''' Get stream URL from songID '''
    results = api_call('getStreamKeyStreamServer', {'songID': songID, 'country':country})
    return results

def get_stream_from_query(query):
    ''' Get stream URL of the most popular song from query '''
    results = get_song_search_results(query)
    songs = results['result']['songs']
    if len(songs) == 0:
        return None, None, None
    
    song = songs[0]
    songID = song['SongID']
    artistName = song['ArtistName']
    songName = song['SongName']
    results = get_stream_key_stream_server(songID)
    url = results['result']['url']
    return url, artistName, songName

class APIError(Exception):
    
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr("There was a problem with your API request: " + self.message)


# if __name__ == '__main__':
#     init()
#     url, artist, title = get_stream_from_query('kanye west')
#     print url, artist, title
