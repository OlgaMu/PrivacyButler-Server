import webapp2
import os

from google.appengine.api import rdbms
from goodle.appengine.ext import webapp

CLOUDSQL_INSTANCE = ' '
DATABASE_NAME = ''
USER_NAME = ''
PASSWORD = ''

def get_connection():
    return rdbms.connect(instance=CLOUDSQL_INSTANCE, database=DATABASE_NAME,
                         user=USER_NAME, password=PASSWORD, charset='utf8')


class MainHandler(webapp2.RequestHandler):
    def post(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (user, site, choice) '
                        'VALUES (%s, %s)',
                        (self.request.get('user'),
                        self.request.get('site'),
                        self.request.get('choice')))
        conn.commit()
        conn.close()
        
        
        
        
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)






