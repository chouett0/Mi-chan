require 'mecab'
require "twitter"
require "uri"

tagger = MeCab::Tagger.new
client = Twitter::REST::Client.new do |config|
	config.consumer_key = 		""
	config.consumer_secret = 	""
	config.access_token = 		""
	config.access_token_secret = 	""

end

wordlist = []

loop{

	timeline = []

	client.home_timeline.each do |tl|
		if !(tl.user == "#<Twitter::User:0x00000002f61a60>")
			frozen_tw = tl.full_text
			tweet = frozen_tw.dup
			
			begin
				URL_scan = tweet.scan URI.regexp(["http", "https"])
				URL_scan[0][1] = "://"
				url = URL_scan.join
				tweet.slice!(url)
			
			rescue
				puts "No URL"

			end

			begin
				tweet.slice!("@")

			end
			
			timeline << tweet

		end

	end

	timeline.each do |tweet|
		w = tagger.parseToNode(tweet)
		begin
			w = w.next
			wordlist << w.surface

		end until w.next.feature.include?("BOS/EOS")
	end

	markov = []

	count = 2

	wordlist.each_cons(count) do |w1, w2|
		sentence = []
		sentence << w1 << w2
		if !(wordlist.include?(sentence))
			print "sentence : #{sentence}\n"
			markov << sentence
		
		end
	end

	text = []
	markov.shuffle!

	markov.each do |w|
	#	print w
	#	print "\n"
	#	print text.length

		if text.length == 0
			text << w[0]
		end

		if text[text.length-1] == w[0]
			text << w[1]
	
		elsif text[0] == w[1]
			text.unshift(w[0])
		
		end

	end

	tw = ""

	tw = text.join

#	client.update(tw)
	print tw

	File.open("talkList.txt", "a") do |file|
		file.puts("*" + tw + "\n")
	
	end

	sleep(10*60)

}
