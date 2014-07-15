import predictionio
import webapp2
import os
import json

from goodle.appengine.ext import webapp
from google.appengine.api import rdbms

client = predictionio.Client(appkey="<app key>")
engine = ''

CLOUDSQL_INSTANCE = ' '
DATABASE_NAME = ''
USER_NAME = ''
PASSWORD = ''


		
class StoreUserChoices(webapp2.RequestHandler):
    def post(self):
		try: 
			client.get_status()
			store_user(self.request.get('user'))
			store_site(self.reuest.get('site'))
			store_choice(self.request.get('choice'))
			status.response.out.write("Saved to prediction data store")
			
		except ServerStatusError:
			conn = get_connection()
			cursor = conn.cursor()
			cursor.execute('INSERT INTO entries (user, site, choice) '
                        'VALUES (%s, %s)',
                        (self.request.get('user'),
                        self.request.get('site'),
                        self.request.get('choice')))
			conn.commit()
			conn.close()
			status.response.out.write("Saved to SQL")
		
	def store_user(uid):
		try:
			client.get_user(uid)
		except predictionio.UserNotFoundError:
			try: 
				client.create_user(uid)
				pass
			except:
				self.response.out.write("problem creating user")
		except:
			self.response.out.write("Unidentified problem with storing the user")	 

	def store_site(site):
		try:
			client.get_item(site)
		except predictionio.ItemNotFoundError:
			try: 
				client.create_item(site)
				pass
			except:
				self.response.out.write("problem creating site")
		except:
			self.response.out.write("Unidentified problem with storing the site")	
		
	def store_choice(uid, site, choice):
		client.identify(uid)
		try:
			client.record_action_on_item("rate", site, {"pio_rate": choice})
		except:
			self.response.oit.write("Problem creating action")

	def get_connection():
		return rdbms.connect(instance=CLOUDSQL_INSTANCE, database=DATABASE_NAME,
							user=USER_NAME, password=PASSWORD, charset='utf8')

   
        

class sendPrediction(webapp2.RequestHandler):
    def get(self):
		uid = self.request.get('uid')
		try:
			client.identify(uid)
			predict = client.aget_itemrec_topn(engine, 5)
			
			try: 	
				results = client.aresp(predict)
				data = json.dumps(results)
				self.response.out.write(data)
			except:
				self.response.out.write("Couldn't make prediction")
			
		except predictionio.ItemRecNotFoundError as e:
			self.response.out.write(e.strerror())
		except:
			self.response.out.write("Something bad happened")
		
	
		
app = webapp2.WSGIApplication([
    ('/storeuserchoices', StoreUserChoices)
	('/getprediction', sendPrediction)
], debug=True)



