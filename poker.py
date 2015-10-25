import httplib
import threading
import re
import time

c_user = ''
xs = ''

headers = {'Cookie': 'c_user=' + c_user + '; xs=' + xs}
resting = False

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
				break
			elif 'sentry' in i[1]:
				print 'Failed to poke ' + self.name + '(' + self.userid + ') - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				global resting
				resting = True
				break

def timer():
	global resting
	if resting == True:
		time.sleep(300)
		resting = False
	threading.Timer(1.0, timer).start()
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
		t.start()

timer()