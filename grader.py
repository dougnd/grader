import glob
import re
import os
import shutil
from datetime import datetime
import sys
import assignment
import inspect


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

    def compile(self, cflags=''):
        cFiles = glob.glob(self.username +"/*.c")

        if len(cFiles) == 0:
            print "ERROR, no .c files!"
            return False

        else:
            print "compiling " + ' '.join(cFiles)

            os.system('gcc {0} -Wall {1} -o "{2}/prog{3}"'.format(
                cflags, ' '.join(('"'+f+'"' for f in cFiles)), self.username, self.progNum))



    def interactiveGrading(self):
        print "Grading for {0}, submitted {1}".format(self.username, self.submittedDate)
        self.compile()
        while True:
            option = raw_input('What should I do? (n,c,e): ')
            if option == 'e':
                exit()
            if option == 'n':
                break
            if option == 'c':
                self.compile()
            if option == 'c99':
                self.compile('-std=c99')


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
    submissions.sort(key = lambda s: s.username)
    print "Found {0} submissions".format(len(submissions))

    try:
        print "Grading for assignment: {0}".format(sys.argv[1])
        prog = getattr(assignment, sys.argv[1])()
    except AttributeError:
        print "Error: could not find program {0}".format(sys.argv[1])
        #knownProgs = (name for name,obj in inspect.getmembers(assignment) if re.search("prog", name))
        knownProgs = (name for name in assignment.__dict__ if re.search("prog", name))
        print "known programs: {0}".format(', '.join(knownProgs))
        exit()

    except IndexError:
        print "Not enough arguments."
        print "usage:"
        print "   grader.py <prog-name> [<commands>]:"
        exit()

    prog.latePoints(submissions[0].submittedDate)
    for s in submissions:
        print "{0} - {1} - {2}".format(s.username, s.submittedDate, prog.latePoints(s.submittedDate))

    exit()

    if len(sys.argv) > 1:
        matches = (s for s in submissions if s.username == sys.argv[1])
        for s in matches:
            s.interactiveGrading()

    else:
        for s in submissions:
            s.interactiveGrading()

