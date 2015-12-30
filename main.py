import webapp2 
from google.appengine.api import users 
from google.appengine.ext import ndb 
from modelli import *
from datetime import datetime, timedelta
from email import email
import logging

def sicurezza(self):
	user = users.get_current_user()
	if user:
		if user.email() == email:
			pass
		else:
			self.redirect('/privato')
	else:
		self.redirect(users.create_login_url("/"))


class ViewHandler(webapp2.RequestHandler): 
	def get(self, fileid): 
		k = ndb.Key(UserFile, fileid) 
		userfile = k.get()
		self.response.headers['Content-Type'] = 'image'
		self.response.write(userfile.filedata) 


class LastHandler(webapp2.RequestHandler):
	def get(self):
		yesterday = datetime.now() - timedelta(1)
		qry = UserFile.query(UserFile.date > yesterday).order(-UserFile.date).fetch(1)
		self.redirect('/view_file/%s' % qry[0].filename)




class PrivatoHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('Questa pagina è privata. Accesso severamente vietato!')

class PuliziaHandler(webapp2.RequestHandler):
	def get(self):
		yesterday = datetime.now() - timedelta(5)
		qry = UserFile.query(UserFile.date < yesterday).order(UserFile.date).fetch(1000)
		for elemento in qry:
			a = elemento.key.delete()

def html(self, mobile=False):	
	yesterday = datetime.now() - timedelta(2)
	qry = UserFile.query(UserFile.date > yesterday).order(-UserFile.date)
	if mobile == True:
		qry = qry.fetch(12)
	testo = ''
	for elemento in qry:
		testo += '<div class="col-xs-6 col-md-2"><a href="/view_file/%s" class="thumbnail"> <img src="/view_file/%s"></a>' % (elemento.filename, elemento.filename)
		testo += '<div class="caption"> <p class="text-info">%s</p> </div> </div>' % elemento.date
	self.response.write('''<!DOCTYPE html>
		<html lang="en">
		  <head>
		    <meta charset="utf-8">
		    <meta http-equiv="X-UA-Compatible" content="IE=edge">
		    <meta name="viewport" content="width=device-width, initial-scale=1">
		    <title>Sicurezza</title>

		    <link href="css/bootstrap.min.css" rel="stylesheet">
		    <!--[if lt IE 9]>
		      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		    <![endif]-->
		  </head>
		  <body>
		  	<div class="container-fluid">
		  		%s
		  	</div>
		    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		    <script src="js/bootstrap.min.js"></script>
		  </body>
		</html>''' % testo)


class MainHandler(webapp2.RequestHandler):
	def get(self):
		sicurezza(self)
		html(self)

class MobileHandler(webapp2.RequestHandler):
	def get(self):
		sicurezza(self)
		html(self, mobile=True)


app = webapp2.WSGIApplication([('/', MainHandler),
								('/privato', PrivatoHandler),
								('/last', LastHandler),
								('/pulizia', PuliziaHandler),
								('/mobile', MobileHandler),
								('/view_file/([^/]+)?', ViewHandler) 
								], debug=True)