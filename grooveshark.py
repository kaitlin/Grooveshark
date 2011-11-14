
import hashlib 
import hmac
import urllib2
import simplejson

KEY = '' #fill in with your key
SECRET = '' #fill in with your secret
API_URL = 'https://api.grooveshark.com/ws3.php?sig='
global SESSION_ID
SESSION_ID = ''

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
    
        
def init():
    #create session
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
              
class APIError(Exception):
    
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr("There was a problem with your API request: " + self.message)
        
        

