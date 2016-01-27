from datetime import datetime
import subprocess

class Assignment(object):
    # dueDate should be of form YYYY-MM-DD
    def __init__(self, dueDate):
        self.dueDate = datetime.strptime(dueDate, '%Y-%m-%d')
        self.testCases = []

    def daysLate(self, date):
        dateDiff = date-self.dueDate
        return max(0,dateDiff.days)

    def latePoints(self, date):
        return 2**self.daysLate(date) - 1

    def runTestCases(self):
        print "ERROR, base class called!"

    def runProg(self, username, arguments=[], stdin='', stdout=False):
        #import ipdb; ipdb.set_trace()
        cmd = [username+'/prog' +str(self.num)]+arguments
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE if stdout else None)
        return proc.communicate(input=stdin)[0]

    def addTestCase(self, name, func):
        def tc(username):
            print "=============================================="
            print " "+name
            print "----------------------------------------------"
            func(username)
            print "----------------------------------------------"
            print " done. "
            print "=============================================="
        self.testCases.append(tc)

    def runTestCases(self, username):
        for tc in self.testCases:
            tc(username)



class prog1(Assignment):
    def __init__(self):
        super(prog1, self).__init__('2016-1-20')
        self.num = 1
        def tc1(username):
            self.runProg(username, stdin="2\n2\n2\n10\n15\n15\n", stdout=True)
            #nums = raw_input("lotto numbers: ")
        self.addTestCase("testing valid inputs: 2 2 2 10 15 15", tc1)


class prog2(Assignment):
    def __init__(self):
        super(prog1, self).__init__('2016-2-1')
        self.num = 2
