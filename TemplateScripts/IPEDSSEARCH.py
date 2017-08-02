import re
class IPEDSSEARCH:
	database = {}

	def init(self):
		file = open("ipeds.txt", "r")
		for line in file:
			ipeds = line[:6]
			institution = re.sub('[ \t\n\r-,&+]', '', line[7:57]).lower()
			self.database[institution] = ipeds
		file.close()
			
	def IPEDSCode(self, nameOfInst):
		if nameOfInst in self.database:
			return self.database[nameOfInst]
		else:
			return "None"