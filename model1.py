from collections import defaultdict
import sys
import time
import pickle

class Modelone(object):
	"""docstring for Model_One"""
	def __init__(self, iter):
		self.iter = iter
		self.count = defaultdict(float)
		self.bigram_count = defaultdict(float)
		self.translation = defaultdict(float)
		self.n_e = dict()
		self.paired_sentences = []
	
	# take 121 sec to run
	def initialize_parameter(self):
		print("initialize parameters")
		# paired_sentence is a list storing tuples with paired sentence
		for pair in self.paired_sentences:
			eng_sentence = pair[0].split()
			for_sentence = pair[1].split()
			for e in eng_sentence:
				for f in for_sentence:
					# if the number of e has been calculated before
					if e in self.n_e:
						self.translation[(f,e)]=1.0/self.n_e[e]
					else:
						# add all foreign words in a SET to avoid duplicate
						different_for_word = set()
						for pair_ in self.paired_sentences:
							if e in pair_[0].split():
								for f_ in pair_[1].split():
									different_for_word.add(f_)
						self.n_e[e]=len(different_for_word)
						self.translation[(f,e)]= 1.0/self.n_e[e]


	def read_corpus(self,english_corpus,foreign_corpus):
		eng_l = english_corpus.readline()
		for_l = foreign_corpus.readline()

		english = []
		foreign = []
		count = 1
		while eng_l and for_l:
		    eline = eng_l.strip()
		    fline = for_l.strip()
		    if eline and fline: # both nonempty lines
		        english.append('NULL '+eline)
		        foreign.append(fline)
		    eng_l = english_corpus.readline()
		    for_l = foreign_corpus.readline()
		    count+=1
		for i in range(len(english)):
			self.paired_sentences.append((english[i],foreign[i]))



	def train(self):
		for iteration in range(self.iter):
			self.bigram_count.clear()
			self.count.clear()
			for pair in self.paired_sentences:
				e = pair[0].split()
				f = pair[1].split()
				for i in range(len(f)):
					for j in range(len(e)):
						delta = self.calculate_delta(f,e,i,j)
						self.bigram_count[(e[j],f[i])] += delta
						self.count[e[j]] += delta
			# revise t(f|e)
			for (f,e) in self.translation:
				self.translation[(f,e)] = self.bigram_count[(e,f)]/self.count[e]
			self.save_parameter(iteration)



	def evaluate(self):
		output = open("dev.out","w")
		for number_of_sentence in range(len(self.paired_sentences)):
			e = self.paired_sentences[number_of_sentence][0].split()
			f = self.paired_sentences[number_of_sentence][1].split()
			for i in range(0,len(f)):
				candidates = []
				# bypass first word NULL
				for j in range(1,len(e)):
					candidates.append((self.translation[(f[i],e[j])],j))

				j = max(candidates,key=lambda item:item[0])[1]
				result = "{} {} {}\n".format(number_of_sentence+1,j,i+1)
				output.write(result)

		output.close()

	# f and e are type of list of words
	def calculate_delta(self,f,e,i,j):
		# summation = self.translation[(f[i],"NULL")]
		summation = 0.0
		for j_ in range(len(e)):
			summation += self.translation[(f[i],e[j_])]
		return self.translation[(f[i],e[j])]/summation



	def save_parameter(self,iter):
		with open('parameters/f2e_translation_iteration_'+str(iter)+'.pkl', 'w') as f:
		    pickle.dump(self.translation, f)
		print "Iteration "+str(iter)+" finished. Translation parameter saved."



	def load_parameter(self,iter):
		with open('parameters/e2f_translation_iteration_'+str(iter-1)+'.pkl') as f:
			self.translation = pickle.load(f)
		print "Translation parameter loaded from translation_iteration_"+str(iter)+".pkl"

def usage():
    print """
    python model1.py [flag] [english corpus] [foreign corpus]
			    	  flag : train/eval
    """

if __name__ == "__main__":
	if len(sys.argv)!=4: # Expect exactly one argument: the training data file
		usage()
		sys.exit(2)

	if sys.argv[1] not in ["train","eval"]:
		usage()
		sys.exit(2)

	try:
		flag    = sys.argv[1]
		english = file(sys.argv[2],"r")
		foreign = file(sys.argv[3],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)

	if flag == "train":
		start = time.time()
		model = Modelone(5)
		model.read_corpus(english,foreign)
		model.initialize_parameter()
		model.train()

		# model.paired_sentences = []
		# model.read_corpus(file("dev.en","r"),file("dev.es","r"))
		# model.evaluate()

		end = time.time()
		# about 10 min
		print "Total training time(sec): "+str(end - start)
	elif flag == "eval":
		start = time.time()
		model = Modelone(5)
		model.read_corpus(english,foreign)
		model.load_parameter(5)
		model.evaluate()
		end = time.time()
		print "Total eval time(sec): "+str(end - start)		

