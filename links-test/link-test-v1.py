import urllib.request, json, csv
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

lineNum = 0
restartAt = 0 # Set to start at a specific line instead... useful for uncaught errors

def checkLink(link):
    result = "N"
    if (len(link) > 5):
        try: 
            openLink = urlopen(link)
        except HTTPError as e:
            result = "HTTPError: " + str(e.code)
        except URLError as e:
            result = "URLError: " + e.reason
        except ValueError as e:
            result = "ValueError"
        else:
            urlCode = openLink.getcode()
            if (urlCode == 200):
                #openLinkSTR = openLink.read()
                #if (not checkForNotFound(openLinkSTR)):
                #    return "Y"
                return "Y"
            else:
                result = urlCode
    return result
    
#def checkForNotFound(text):
#    return ("404" in text or "Not Found" in text)

# "N" means invalid link
# (Code) means HTTP message thrown that was not 200 (Response OK)
# "Not Found" means the words "Not found" or "404" were found on the page
# Y means probably legit

read = open("in.csv", "r").read().split('\n')
with open("out.csv", "a", newline='') as file:
    out = csv.writer(file)
    for line in read:
        lineNum += 1
        if (restartAt < lineNum): # if Restart is set, skip till you get there..
            strip = line.split(',')
            left = strip[0].replace('"','')
            right = strip[1].replace('"','') # Strip quotes, which are added when URLs have commas
            leftPrint = checkLink(left)
            rightPrint = checkLink(right)
            file.write(left + "," + right + "," + leftPrint + "," + rightPrint + "\n")
            if (leftPrint != "Y"):
                print ("Left@" + str(lineNum) + ": " + leftPrint)
            if (rightPrint != "Y"):
                print ("Right@" + str(lineNum) + ": " + rightPrint)
            if (leftPrint == "Y" and rightPrint == "Y"):
                print ("@" + str(lineNum) + ": OK ")

