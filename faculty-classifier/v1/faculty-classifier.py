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
		if (len(row[0]) < 3) and not(training): # only train on non-blanks
				dataset.append([""])
		else:
			if (training):
				dataset.append((row[0].lower(), row[1]))
			else:
				dataset.append([row[0]])
	return dataset

print("\r\n#### Training Set ####")
training = getDataset("data/training-data.csv", 1)
print("Training on " + str(len(training)) + " samples from training-data")
cl = NaiveBayesClassifier(training)
print("Trained on training-data")

print("\r\n#### Testing Set ####")
test = getDataset("data/test-data.csv", 1)
print("Testing on " + str(len(test)) + " samples from test-data")
print("Tested on test-data completed with accuracy: {0}".format(cl.accuracy(test)) + ", now training")
cl.update(test)
print("Trained on test-data")

print("\r\n#### Features ####")
print(cl.show_informative_features(15))

print("\r\n#### Full Classification ####")
with open("data/partial-randomized-faculty-data.csv", 'r') as inputFile:
	random = csv.reader(inputFile, delimiter=",", quotechar='"')
	print("Classifying partial-randomized-faculty-data")
	with open("data/partial-randomized-faculty-data-out.csv", "w", newline='') as outputFile:
		randomResults = [0, 0, 0, 0]
		averageProb = 0
		totalChecked = 0
		randomOut = csv.writer(outputFile, delimiter=",", quotechar='"')
		for row in random:
			result = 4
			if (len(row) > 0 and len(row[0]) >= 3):
				randomTitle = row[0].lower()
				prob_dist = cl.prob_classify(randomTitle)
				result = prob_dist.max()
				prob = round(prob_dist.prob(result), 3)
				print("'" + randomTitle + "': " + result + " @ " + str(prob))
				averageProb += prob
				totalChecked += 1
			randomOut.writerow([row, result])
			randomResults[int(result)-1] += 1
	print("Completed partial-randomized-faculty-data classification")
	print("Classes (1): " + str(randomResults[0]) + ", (2): " + str(randomResults[1]) + ", (3): " + str(randomResults[2]) + ", (4): " + str(randomResults[3]))
	if (totalChecked >= 0): 
		print("Average Certainty: " + str(averageProb / totalChecked))

print("\r\n#### Input Test ####")
prompt = ""
while not(prompt == "stop"):
	prompt = input("Position: ")
	word = prompt.lower()
	res = TextBlob(word, classifier=cl).classify()
	print("'" + word + "': " + str(res) + " ("+ interpret(res) + ")\r\n")