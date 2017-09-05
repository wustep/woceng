import urllib.request, json, csv, requests, configparser
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

config = configparser.ConfigParser()
try: 
    config.read('config.cfg')
    faceAPIKey = config['Face++']['API_KEY']
    faceAPISecret = config['Face++']['API_SECRET']
except:
    print("Error occurred reading config. Please create a 'config.cfg' file with the following text:")
    print("[Face++]")
    print("API_KEY=YOUR_API_KEY_HERE")
    print("API_SECRET=YOUR_API_SECRET_HERE")
    exit()

lineNum = 1
restartAt = 2 # Set to start at a specific line instead... useful for uncaught errors or interrupts
# leave newline on end of out file though when restarting
inFile = input("Input file name?: ")
outFile = input("Output file name?: ")

def checkLink(link):
    result = "N"
    if (len(link) > 5):
        try: 
            openLink = urlopen(link)
        except HTTPError as e:
            result = "HTTPError: " + str(e.code)
        except URLError as e:
            result = "URLError"
        except ValueError as e:
            result = "ValueError"
        except TimeoutError as e:
            result = "TimeoutError"
        except SSLError as e:
            result = "SSLError"
        except InvalidURL as e:
            result = "InvalidURL"
        except NameError as e:
            result = "NameError"
        except:
            result = "UnexpectedError: " + sys.exec.info()[0]
        else:
            urlCode = openLink.getcode()
            if (urlCode == 200):
                return "OK"
            else:
                result = urlCode
    return result
    
#def checkForNotFound(text):
#    return ("404" in text or "Not Found" in text)

# "N" means invalid link
# (Code) means HTTP message thrown that was not 200 (Response OK)
# "Not Found" means the words "Not found" or "404" were found on the page
# Y means probably legit

with open(inFile, 'r') as inputFile:
    read = csv.reader(inputFile, delimiter=",", quotechar='"')
    with open(outFile, "w", newline='') as outputFile:
        out = csv.writer(outputFile, delimiter=",", quotechar='"')
        for row in read:
            if (restartAt <= lineNum): # if Restart is set, skip till you get there..
                line = ""
                gender = ""
                ethnicity = ""
                leftPrint = "BLANK"
                if (len(row) > 0):
                    line = row[0]
                    leftPrint = checkLink(line)
                    if (leftPrint == "OK"):
                        files = [
                            ('api_key', faceAPIKey),
                            ('api_secret', faceAPISecret),
                            ('image_url', row[0]),
                            ('return_landmark', '1'),
                            ('return_attributes', 'gender,ethnicity')
                        ]
                        res = requests.post("https://api-us.faceplusplus.com/facepp/v3/detect", data=files, headers={'User-Agent' : 'py'})
                        if res.status_code == 200:
                            d = json.loads(res.content)
                            if (len(d["faces"]) > 0):
                                if (len(d["faces"]) > 1):
                                    print("@" + str(lineNum) + "More than 1 face found")
                                gender = (d["faces"][0]["attributes"]["gender"]["value"])
                                ethnicity = (d["faces"][0]["attributes"]["ethnicity"]["value"])
                            else:  
                                leftPrint = "Face++ Face Not Found"
                        else: 
                            leftPrint = "Face++ " + str(res.status_code)
                out.writerow([line, leftPrint, gender, ethnicity])
                print ("@" + str(lineNum) + ": " + leftPrint + " " + gender + " " + ethnicity)
            lineNum += 1
