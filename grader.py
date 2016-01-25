import glob
import re
import os
import shutil
from datetime import datetime
import sys


class Submission(object):
    def __init__(self, txtFileName, progNum):
        self.loadFromFile(txtFileName)
        self.processFiles()
        self.progNum = progNum

    def loadFromFile(self, txtFileName):
        #print "processing " + txtFileName
        txtContents = open(txtFileName, "r").read()

        m = re.match("Name: (.+) \((\w+)\)", txtContents)
        if m:
            self.fullName = m.group(1)
            self.username = m.group(2)
            #print "Processing " + self.fullName + ", " +self.username
        else:
            raise Exception("Could not find name in txt file: " + txtFileName)
        
        m = re.search("Date Submitted: (.+)$", txtContents, re.MULTILINE)
        if m:
            self.submittedDate = datetime.strptime(m.group(1), "%A, %B %d, %Y %I:%M:%S %p %Z")
        else:
            raise Exception("Could not find date in txt file: " + txtFileName)

        self.fileNames = re.findall("Original filename: (.+)$", txtContents, re.MULTILINE)
        self.mangledNames = re.findall("Filename: (.+)$", txtContents, re.MULTILINE)

        if len(self.mangledNames) != len(self.fileNames):
            raise Exception("Error processing files for txt file: " + txtFileName)
        #print self.mangledNames
        #print self.fileNames

    def compile(self):
        cFiles = glob.glob(self.username +"/*.c")

        if len(cFiles) == 0:
            print "ERROR, no .c files!"

        elif len(cFiles) == 1:
            print "compiling " + cFiles[0]
            os.system("gcc -Wall {0} -o {1}/prog{2}".format(cFiles[0], self.username, self.progNum))

        else:
            #objfiles = [f+'.o' for f in cFiles]
            #for f,o in zip(cFiles, objfiles):
                #print "compiling " + f
                #os.system("gcc -Wall -c {0} -o {1}".format(f, o))


            os.system("gcc -Wall {0} -o {1}/prog{2}".format(' '.join(cFiles), self.username, self.progNum))



        



    def interactiveGrading(self):
        print "Grading for {0}, submitted {1}".format(self.username, self.submittedDate)
        self.compile()

    def processFiles(self):
        if not os.path.exists(self.username):
            os.makedirs(self.username)

        for m,f in zip(self.mangledNames, self.fileNames):
            if not os.path.exists(self.username+ "/"+f):
                shutil.copy("zip/"+m, self.username+ "/"+f)



def processZip():
    txtFiles = glob.glob("zip/*.txt")
    #print txtFiles
    #print len(txtFiles)
    submissions = []
    for f in txtFiles:
        submissions.append(Submission(f, 1))
    return submissions





if __name__ == "__main__":
    submissions = processZip()
    print "Found {0} submissions".format(len(submissions))

    if len(sys.argv) > 1:
        matches = (s for s in submissions if s.username == sys.argv[1])
        for s in matches:
            s.interactiveGrading()

    else:
        for s in submissions:
            s.interactiveGrading()
