from google.appengine.ext import ndb 

class UserFile(ndb.Model): 
	filename = ndb.StringProperty() 
	filedata = ndb.BlobProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)