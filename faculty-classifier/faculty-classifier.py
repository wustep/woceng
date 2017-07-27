# Adapted from http://stevenloria.com/how-to-build-a-text-classification-system-with-python-and-textblob/ 

import csv
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

# clean function - may not be necessary, lower is probably good enough.. tests to be done
#words = ["\"", "engineering", "for", "nuclear", "in", "alumni", "the", "|", "ce", "ece", "chemical", "medicine", "to", "public", "policy", "computation", "biomedical", "electrical", "environmental", "mechanical", "engineering", "computer", "program", "aerospace" "electrical", "and", "systems", "sensors", "of", "&", "civil", "environment", "safety", "chemistry", "biological", "ece", "/", "department", "physical", "rehabilitation", "science", "mineral", "physics", "astronomy"] # get rid of unnecessary words
#def clean(str):
#	split = str.split()
#	result = ""
#	for word in split:
#		adj = word.lower().replace(",","").replace("(","").replace(")","")
#		if not(adj in words):
#			result += adj + " "
#	return result.strip()
			
def interpret(res):
	if (str(res) == "1"):
		return "tenure-track or tenured faculty"
	elif (str(res) == "2"):
		return "non-tenure-track faculty"
	elif (str(res) == "3"):
		return "support staff"
	else:
		return "invalid"

def getDataset(filename, training=0): # Returns csv in array if training=0, otherwise returns csv in cleaned array with removed blanks
	f = open(filename)
	c = csv.reader(f)
	next(c)
	
	dataset = []

	for row in c:
		if (not(training) or len(row[0]) > 3): # Only train on non-blanks
			if training:
				dataset.append((row[0].lower(), row[1]))
			else:
				dataset.append(row[0])
	return dataset

print("#### Training Set ####")
training = getDataset("training-data.csv", 1)
cl = NaiveBayesClassifier(training)
print("Trained on " + str(len(training)) + " samples from training-data")

print("#### Testing Set ####")
test = getDataset("test-data.csv", 1)
print("Testing on " + str(len(test)) + " samples from test-data")
print ("Accuracy: {0}".format(cl.accuracy(test)))
cl.update(test)
print("Trained on test-data")

print("#### Features ####")
print(cl.show_informative_features(15))

#print ("#### Random Tests ####")
#random = getDataset("partial-randomized-faculty-data.csv", 0)
#for row in random:
#	randomTitle = row.lower()
#	result = 4
#	if (len(randomTitle) >= 3):
#		result = TextBlob(randomTitle, classifier=cl).classify()
#	print("'" + randomTitle + "': " + str(result))

print("\r\n#### Input Test ####")
prompt = ""
while not(prompt == "stop"):
	prompt = input("Position: ")
	word = prompt.lower()
	res = TextBlob(word, classifier=cl).classify()
	print("'" + word + "': " + str(res) + " ("+ interpret(res) + ")")