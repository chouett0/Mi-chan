# _*_ coding: utf-8 _*_
import twitter
import MySQLdb
from time import sleep
import re
"""
def remake(text):
	slice = text[0:1]
	while slice != " ":
		slice= text[0:1]
		text = text.lstrip(slice)
		print text

	f = text.find("RT")
	if f != -1:
		while f == -1:
			slice = text[0:1]
			text = text.lstrip(slice)
			text.find("RT")

	return text
"""

def reply():
	try:
		KEY_list = ["",
		"",
		"",
		""
		]

		api = twitter.Api(KEY_list[0], KEY_list[1], KEY_list[2], KEY_list[3])

	except:
		print "OAuth error"

	name = re.compile("@mi_chan_823 ")

	since = 0

	connecter = MySQLdb.connect(host="localhost", user="", passwd="", db="Tweet", charset="utf8")
	csr = connecter.cursor()

	tl = api.GetHomeTimeline(since_id=since)
	for tweet in tl:
		since = tweet.id
		csr.execute("SELECT Tweet FROM Wordlist ORDER BY RAND() LIMIT 1")
		word = csr.fetchone()
		print word

		if name.search(tweet.text) is not None:
			text = "@" + tweet.user.screen_name + " " + word
			api.PostUpdate(text, in_reply_to_status_id=tweet.id)				
			print "posted to " + tweet.user.screen_name + word
	"""		
	except:
		print "Post error"
	"""

def collect():	
	KEY_list = [
	]
	api = twitter.Api(KEY_list[0], KEY_list[1], KEY_list[2], KEY_list[3])

	since = 0
	
	connecter = MySQLdb.connect(host="localhost", user="", passwd="", db="Tweet", charset="utf8")
	csr = connecter.cursor()
	tl = api.GetHomeTimeline(since_id=since)

	for tweet in tl:
		since = tweet.id
		id = tweet.user.screen_name
		tweet = tweet.text
		mean = "none"
		slice = tweet[0:1]
		if slice == "@":
			tweet = remake(tweet)

		data = (id, tweet, mean)
		sql = u"insert into Wordlist(ID, Tweet, Mean) values(%s,%s,%s)"
		try:
			csr.execute(sql, data)
		except:
			continue

		print id, tweet, mean

	connecter.commit()

def Check_port(flag):
 #check_port

 Port = [80, 110, 442, 3329, 3333]
 for p in Port:
 try:
  s = socket(AF_INET, SOCK_STREAM,0)
  s.settimeout(1)
  s.connect*1
  print str(p) + ':OK'
  s.close()
  flag = 1
 except error, msg:
  print str(p) + ':' + str(msg)
  flag = -1
 Return 

def send_ping():
 #send_ping

def send_MagicPacket()
 #send_MPacket

if __name__ == "__main__":
 while True:
# Check_flag = Port_check()
 if Port_check() > 0:
  time.sleep(30)

 else:
  check_flag = send_ping()
  report("port error")
   if check_flag > 0:
    sys.exit()

   else:
     check_flag = send_MagicPacket()
     report("Can't ping")
     if check_flag > 0:
      sys.exit()

     else:
      report("Can't Access Server")
      sys.exit()
     
 
	
