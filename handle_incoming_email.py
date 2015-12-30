import logging
import webapp2
from modelli import *
import urllib
from datetime import datetime
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import memcache
from email import token

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
    	if hasattr(mail_message, 'attachments'):
	        for elemento in mail_message.attachments:
				userfile = UserFile( id=elemento.filename, filename=elemento.filename, filedata=str(elemento.payload.decode())) 
				userfile.put()
				data = memcache.get('test')
				if data is None: 
					url = "https://maker.ifttt.com/trigger/sicurezzacam/with/key/" + token
					form_fields = {"value1": datetime.now(), "value2": elemento.filename}
					form_data = urllib.urlencode(form_fields)
					result = urlfetch.fetch(url=url,
					    payload=form_data,
					    method=urlfetch.POST,
					    headers={'Content-Type': 'application/x-www-form-urlencoded'})
					memcache.add(key="test", value="1", time=60)
		else:
			logging.info('Ciccio')




app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)