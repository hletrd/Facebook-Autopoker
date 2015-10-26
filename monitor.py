db = 'log.db'

import sqlite3
import time

dbc = sqlite3.connect(db, check_same_thread=False)
dbc.text_factory = str
c = dbc.cursor()

def key(obj):
	return obj[2]

while True:
	c.execute('SELECT userid, name, COUNT(`date`) FROM log WHERE `date` > \'' + time.strftime('%Y-%m-%d 00:00:00') + '\' AND result=1 GROUP BY userid;')
	result = c.fetchall()
	result.sort(key=key, reverse=True)

	total = 0
	for i in result:
		total += i[2]
		print('Poked ' + str(i[1]) + '(' + str(i[0]) + ') ' + str(i[2]) + ' times today')
	print('Total: ' + str(total) + ' pokes')

	c.execute('SELECT COUNT(`date`) FROM log WHERE `date` > datetime(\'' + time.strftime('%Y-%m-%d %H:%M:%S') + '\', \'-24 hours\') AND result=1;')
	print(str((c.fetchone()[0] * 100 / 1440) / 100.0) + ' ppm for last 24 hours')
	c.execute('SELECT COUNT(`date`) FROM log WHERE `date` > datetime(\'' + time.strftime('%Y-%m-%d %H:%M:%S') + '\', \'-1 hours\') AND result=1;')
	print(str((c.fetchone()[0] * 100 / 60) / 100.0) + ' ppm for last 1 hour')
	c.execute('SELECT COUNT(`date`) FROM log WHERE `date` > datetime(\'' + time.strftime('%Y-%m-%d %H:%M:%S') + '\', \'-5 minutes\') AND result=1;')
	print(str((c.fetchone()[0] * 100 / 5) / 100.0) + ' ppm for last 5 minutes')

	print('')
	time.sleep(5)