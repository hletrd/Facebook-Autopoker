c_user = ''
xs = ''
db = 'log.db'

try:
	import httplib
	python3 = False
except:
	import http.client
	python3 = True
import threading
import re
import time
import sqlite3

headers = {'Cookie': 'c_user=' + c_user + '; xs=' + xs}
resting = False
poking = []

dbc = sqlite3.connect(db, check_same_thread=False)
dbc.text_factory = str
c = dbc.cursor()
try:
	c.execute('CREATE TABLE log(date TEXT, name TEXT, userid TEXT, result INT)')
except:
	pass
dbc.commit()
dbc.close()

class poke(threading.Thread):
	def __init__(self, url, name, userid):
		threading.Thread.__init__(self)
		self.url = url
		self.name = name
		self.userid = userid
		self.dbc = sqlite3.connect(db, check_same_thread=False)
		self.dbc.text_factory = str
		self.c = self.dbc.cursor()

	def run(self):
		global resting, poking
		if resting == True:
			return
		if python3 == True:
			conn = http.client.HTTPSConnection('m.facebook.com')
		else:
			conn = httplib.HTTPSConnection('m.facebook.com')
		conn.request('GET', '/pokes/inline/' + self.url, '', headers)
		resp = conn.getresponse()
		rest = resp.read()
		resp_headers = resp.getheaders()
		for i in resp_headers:
			if 'success' in i[1]:
				print('Poked ' + self.name + '(' + self.userid + ') - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				self.c.execute('INSERT INTO log VALUES (?, ?, ?, ?)', (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.name, self.userid, 1))
				self.dbc.commit()
				self.dbc.close()
				break
			elif 'sentry' in i[1]:
				resting = True
				print('Failed to poke ' + self.name + '(' + self.userid + ') - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				self.c.execute('INSERT INTO log VALUES (?, ?, ?, ?)', (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.name, self.userid, 0))
				self.dbc.commit()
				self.dbc.close()
				break
			elif 'pending' in i[1]:
				break

class refresh(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global resting
		if resting == True:
			time.sleep(300)
			resting = False
		threading.Timer(0.5, run_once).start()
		if python3 == True:
			conn = http.client.HTTPSConnection('m.facebook.com')
		else:
			conn = httplib.HTTPSConnection('m.facebook.com')
		conn.request('GET', '/pokes', '', headers)
		resp = conn.getresponse()
		rest = resp.read()
		if python3 == True:
			rest = rest.decode()
		links = re.findall(r'href="\/pokes\/inline\/([^"]+)">', rest)
		names = re.findall(r'<a href="\/([^"]+)">([^<]+)<', rest)

		for i, j in enumerate(links):
			userid = names[i][0]
			if 'profile.php?id=' in userid:
				userid = re.search(r'[0-9]+', userid).group(0)
			t = poke(j.replace('&amp;', '&'), names[i][1], userid)
			t.daemon = True
			t.start()

def run_once():
	w = refresh()
	w.daemon = True
	w.start()

if __name__ == '__main__':
	run_once()
	while True:
		time.sleep(1)