import scipy as sp
import nltk
import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

english_stemmer = nltk.stem.SnowballStemmer('english')

def dist_raw(v1, v2):
	delta = v1 - v2
	return sp.linalg.norm(delta.toarray())

def dist_norm(v1, v2):
	v1_normalized = v1/sp.linalg.norm(v1.toarray())
	v2_normalized = v2/sp.linalg.norm(v2.toarray())

	delta = v1_normalized - v2_normalized

	return sp.linalg.norm(delta.toarray())

def tokenize(content):
        tagger = MeCab.Tagger('-Ochasen')
        node = tagger.parseToNode(content)
        wordlist = ""

        while node:
                if node.surface != "*":
                        wordlist += node.surface + " "
                node = node.next

        return wordlist

def get_wordlist(content):
        return [tokenize(list) for list in content if list]

def get_words(content):
        ret = []
        for s in get_wordlist(content):
                if s:
                        ret.append(s)

        return ret

class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
        	return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))
