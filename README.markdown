#Grooveshark Public API Wrapper

This is a pretty simple wrapper for the grooveshark public api. To use it, you'll need an api key and secret pair. You can request this [on their developer site](http://developers.grooveshark.com/api).  


To get started, fill in the KEY and SECRET variables with your own. Then, initialize a session:  

```
import grooveshark  
grooveshark.init()  

```
  

You can now use the api_call method to make requests. Required parameters are the api method name, and a dictionary of parameters required for that method. For example:  

```
grooveshark.api_call('getSongSearchResults', {'query': 'la vie en rose', 'country': 'USA'})
```  

To make api calls that require user authentication, call the authenticate_user method:  

```
grooveshark.authenticate_user(username, password)
```  

Get stream URL, artist, and title of the most popular song based on query:

```
url, artist, title = grooveshark.get_stream_from_query('kanye west')
```

For more information on the grooveshark API methods and their required parameters, visit the [grooveshark documentation](http://developers.grooveshark.com/docs/public_api/v3/)


