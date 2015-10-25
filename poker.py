import httplib
import threading
import re
import time
import sqlite3

c_user = ''
xs = ''
db = 'log.db'

headers = {'Cookie': 'c_user=' + c_user + '; xs=' + xs}
resting = False
dbc = sqlite3.connect(db, check_same_thread=False)
dbc.text_factory = str
c = dbc.cursor()
try:
	c.execute('CREATE TABLE log(date TEXT, name TEXT, userid TEXT, result INT)')
except:
	pass

class poke(threading.Thread):
	def __init__(self, url, name, userid):
		threading.Thread.__init__(self)
		self.url = url
		self.name = name
		self.userid = userid

	def run(self):
		conn = httplib.HTTPSConnection('m.facebook.com')
		conn.request('GET', '/pokes/inline/' + self.url, '', headers)
		resp = conn.getresponse()
		rest = resp.read()
		resp_headers = resp.getheaders()
		for i in resp_headers:
			if 'success' in i[1]:
				print 'Poked ' + self.name + '(' + self.userid + ') - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				c.execute('INSERT INTO log VALUES (?, ?, ?, ?)', (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.name, self.userid, 1))
				dbc.commit()
				break
			elif 'sentry' in i[1]:
				print 'Failed to poke ' + self.name + '(' + self.userid + ') - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				c.execute('INSERT INTO log VALUES (?, ?, ?, ?)', (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.name, self.userid, 0))
				dbc.commit()
				global resting
				resting = True
				break

def timer():
	global resting
	if resting == True:
		time.sleep(300)
		resting = False
	threading.Timer(0.5, timer).start()
	conn = httplib.HTTPSConnection('m.facebook.com')
	conn.request('GET', '/pokes', '', headers)
	resp = conn.getresponse()
	rest = resp.read()
	links = re.findall(r'href="\/pokes\/inline\/([^"]+)">', rest)
	names = re.findall(r'<a href="\/([^"]+)">([^<]+)<', rest)

	for i, j in enumerate(links):
		userid = names[i][0]
		if 'profile.php?id=' in userid:
			userid = re.search(r'[0-9]+', userid).group(0)
		t = poke(j.replace('&amp;', '&'), names[i][1], userid)
		t.daemon = True
		t.start()

timer()