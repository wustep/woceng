# Adapted from http://stevenloria.com/how-to-build-a-text-classification-system-with-python-and-textblob/ 

import csv
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob 

# Returns interpretation of faculty designation
def interpretFaculty(res):
	if (str(res) == "1"):
		return "tenure-track or tenured faculty"
	elif (str(res) == "2"):
		return "non-tenure-track faculty"
	elif (str(res) == "3"):
		return "not staff"
	else:
		return "invalid"

# Returns interpretation of staff designation
def interpretStaff(res):
	if (str(res) == "1"):
		return "administrator"
	elif (str(res) == "2"):
		return "staff"
	elif (str(res) == "3"):
		return "not staff"
	else:
		return "invalid"

# Reads data from CSV and puts into dataset array
# Column = 1 for faculty, 2 for staff designation
# Training = 1 for test/training set, 0 otherwise
def getDataset(filename, column=1, training=0): 
	f = open(filename)
	c = csv.reader(f)
	next(c)
	
	dataset = []
	next(c, None)  # skip the headers
	for row in c:
		if (len(row[0]) < 3): # Invalid input
			if not(training): # Don't bother if it's training
				dataset.append([""]) 
		else:
			if (training):
				res = row[column]
				if (res == ""): # 3 means NOT staff / faculty. These are blank in training data for readability
					res = 3
				dataset.append([row[0], res]) 
			else:
				dataset.append([row[0]])
	return (dataset)

print("\r\n#### Training Set ####")
trainFacultyData = getDataset("data/training-data.csv", 1, 1)
trainStaffData = getDataset("data/training-data.csv", 2, 1)
print("Training on " + str(len(trainStaffData)) + " samples from training-data")
facultyClassifier = NaiveBayesClassifier(trainFacultyData)
print("Trained faculty classifier on training-data")
staffClassifier = NaiveBayesClassifier(trainStaffData)
print("Trained staff classifier on training data")

print("\r\n#### Test Set ####")
testFacultyData = getDataset("data/test-data.csv", 1, 1)
testStaffData = getDataset("data/test-data.csv", 2, 1)
print("Testing on " + str(len(testStaffData)) + " samples from test-data")
print("Faculty Accuracy: {0}".format(facultyClassifier.accuracy(testFacultyData)))
print("Staff Accuracy: {0}".format(staffClassifier.accuracy(testStaffData)))

print("Updating faculty classifier...")
facultyClassifier.update(testFacultyData)
print("Updating staff classifier...")
staffClassifier.update(testStaffData)
print("Classifiers updated.")

print("\r\n#### Features ####")
print("Faculty Classifier")
print(facultyClassifier.show_informative_features(15))
print("Staff Classifier")
print(staffClassifier.show_informative_features(15))

inputFileName = input('Enter input file name (e.g. data/partial-randomized-faculty-data.csv):');
outputFileName = input('Enter output file name:');

print("\r\n#### Full Classification ####")
with open(inputFileName, 'r') as inputFile:
	reader = csv.reader(inputFile, delimiter=",", quotechar='"')
	print("Classifying partial-randomized-faculty-data")
	with open(outputFileName, "w", newline='') as outputFile:
		facultyResults = [0, 0, 0, 0]
		facultyAverageProb = 0
		staffResults = [0, 0, 0, 0]
		staffAverageProb = 0
		totalChecked = 0
		output = csv.writer(outputFile, delimiter=",", quotechar='"')
		next(reader, None)  # skip the headers
		for row in reader:
			staffResult = 4
			facultyResult = 4
			line = ""
			if (len(row) > 0):
				line = row[0]
			if (len(line) >= 3):
				title = row[0].lower()
				facultyProbDist = facultyClassifier.prob_classify(title)
				facultyResult = facultyProbDist.max()
				facultyProb = round(facultyProbDist.prob(facultyResult), 3)
				staffProbDist = staffClassifier.prob_classify(title)
				staffResult = staffProbDist.max()
				staffProb = round(staffProbDist.prob(staffResult), 3)
				if (facultyProb < 0.5 or staffProb < 0.5):
					print("'" + title + "': " + str(staffResult) + ", " + str(facultyResult) + " @ " + str(facultyProb) + ", " + str(staffProb))
				facultyAverageProb += facultyProb
				staffAverageProb += staffProb
				totalChecked += 1
			output.writerow([line, facultyResult, staffResult])
			facultyResults[int(facultyResult)-1] += 1
			staffResults[int(staffResult)-1] += 1
	print("Completed partial-randomized-faculty-data classification")
	print("Faculty classes (1): " + str(facultyResults[0]) + ", (2): " + str(facultyResults[1]) + ", (3): " + str(facultyResults[2]) + ", (4): " + str(facultyResults[3]))
	print("Staff classes (1): " + str(staffResults[0]) + ", (2): " + str(staffResults[1]) + ", (3): " + str(staffResults[2]) + ", (4): " + str(staffResults[3]))
	if (totalChecked >= 0): 
		print("Faculty Average Certainty: " + str(facultyAverageProb / totalChecked))
		print("Staff Average Certainty: " + str(staffAverageProb / totalChecked))

print("\r\n#### Input Test ####")
prompt = ""

while not(prompt == "stop"):
	prompt = input("Position: ")
	word = prompt.lower()
	res = TextBlob(word, classifier=facultyClassifier).classify()
	res2 = TextBlob(word, classifier=staffClassifier).classify()
	print("'" + word + "': " + str(res) + " ("+ interpretFaculty(res) + "), " + str(res2) + " (" + interpretStaff(res2) + ")\r\n")