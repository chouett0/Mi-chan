# _*_ coding: utf-8 _*_
import os
import sys
import csv
import twitter
import re
from time import sleep
from function import *
posts_dataset = []

if __name__ == "__main__":
	try:
	    	KEY_list = ["CT",
	                "CS",
	                "AT",
	                "AC"]

	        api = twitter.Api(KEY_list[0], KEY_list[1], KEY_list[2], KEY_list[3])

	except Exception as e:
	        print "==========Error=========="
	        print e.args[0]
		print "OAuth Error"
		print "========================="

	since=0


	with open("./LINE_dataset.csv", "rb") as f:
	               	reader = csv.reader(f)
	                for line in reader:
	                        posts_dataset.append(line)

	posts_row = []
	sumire_row = []

	for sentence in posts_dataset:
		if len(sentence[0])/3 >= 6:
			posts_row.append(sentence[0])
			sumire_row.append(sentence[1])

	posts = get_words(posts_row)

	posts_dict = {}
	for i in range(len(posts)-1):
	        posts_dict[i] = posts[i]

	sumire_posts = get_words(sumire_row)

	from sklearn.feature_extraction.text import CountVectorizer
	vectorizer = StemmedTfidfVectorizer(min_df=1, stop_words='english')

	X_train = vectorizer.fit_transform(posts)
	mmzuku_num, mmzuku_features = X_train.shape

	while True:
		timeline = api.GetHomeTimeline(since_id=since)

		for tl in timeline:
			tweet = tl.text
			since = tl.id
			if re.match("@mi_chan_823", tweet):

				try:
					sentence = re.sub("@mi_chan_823", "", tweet)
					sentence = sentence.strip()
					reply_to = tl.user.screen_name

					new_post = str(tweet)
					new_post_vec = vectorizer.transform(get_words([new_post]))

					best_doc = None
					best_dist = sys.maxint
					best_i = None

					for i in range(0, mmzuku_num):
						post = posts[i]

						post_vec = X_train.getrow(i)
						d = dist_norm(post_vec, new_post_vec)

						print "=== Post %i with dist=%.2f: %s" % (i, d, post)

						if d < best_dist:
							best_dist = d
							best_i = i
							best_doc = post

					print "Best post is %i with dist=%.2f: %s %d" % (best_i, best_dist, best_doc, len(best_doc))

					best_reply_num = posts_dict.keys()[posts_dict.values().index(best_doc)]
					reply = sumire_row[best_reply_num]
					print sentence + " → " + reply

					rep = "@" + reply_to + " " + reply
					api.PostUpdate(status=rep, in_reply_to_status_id=tl.id)
				except:
					pass
		sleep(5*60)
