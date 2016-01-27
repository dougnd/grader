from datetime import datetime

class Assignment(object):
    # dueDate should be of form YYYY-MM-DD
    def __init__(self, dueDate):
        self.dueDate = datetime.strptime(dueDate, '%Y-%m-%d')

    def daysLate(self, date):
        dateDiff = date-self.dueDate
        return max(0,dateDiff.days)

    def latePoints(self, date):
        return 2**self.daysLate(date) - 1

class prog1(Assignment):
    def __init__(self):
        super(prog1, self).__init__('2016-1-20')

class prog2(Assignment):
    def __init__(self):
        super(prog1, self).__init__('2016-2-1')
