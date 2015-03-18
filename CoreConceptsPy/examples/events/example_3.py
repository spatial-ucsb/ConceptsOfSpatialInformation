#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Operations on UCSB course data of Winter Quarter 2014 as examples for how to use the core concept 'event'

Use Cases:
- Do courses take place at the same location at the same time?
- Imagine a person with a course schedule of 5 courses (5 randomly selected courses).
    Does any of these courses overlap with another course or is during another course?
    Which courses are after a certain course on a certain day?
    Which courses are before a certain course on a certain day?
    What is the next date and time for a certain course?


Provided data:
CSV file with all courses of the UCSB Winter Quarter 2014
The fields for each course are:
Term,Session,Acad Group,Class Nbr,Subject,Catalog Nbr,Section,Course Title,Component,Codes,M,T,W,TH,F,S,SU,Start Date,End Date,Time,Location,Instructor,Units,

"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "January 2015"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from events import *
import dateutil.parser
from datetime import *
from random import randrange
import csv

log = _init_log("example-3")

events = []

f = open('../data/events/course_data.csv')
reader = csv.DictReader(f)

def getWeekDayName(weekDayNumber):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[weekDayNumber]

def getWeekDays(event):
    '''
    @param event an event
    @return array of integers for the weekdays of this course (0-6 = Monday - Sunday)
    '''
    weekDays = {'M': 0, 'T': 1, 'W': 2, 'TH': 3, 'F': 4, 'S': 5, 'SU': 6}
    activeWeekDays = []
    for w in weekDays:
        if event.get(w):
            activeWeekDays.append(weekDays[w])

    return activeWeekDays

def getHours(abbrDuration):
    '''
    @param abbrDuration abbreviated duration of the course
    @return array[datetime.time] holds the start time and end time of the course
    '''
    duration, period = abbrDuration[:-2], abbrDuration[-2:]
    print duration
    print period

    times = duration.split('-')
    timeArr = []

    for x in range(0, 2):
        if len(times[x]) > 2:
            times[x] = times[x][:-2] + ' ' + times[x][-2:]
        else:
            times[x] = times[x] + ' 00'

        t = datetime.strptime(times[x] + ' ' + period, "%I %M %p")

        timeArr.append(time(t.hour, t.minute))

        if x == 1 and period == "PM" and timeArr[1].hour < timeArr[0].hour:
            timeArr[0] = timeArr[0].replace((timeArr[0].hour + 12)%24, timeArr[0].minute)

    return timeArr




for row in reader:
    startTime = dateutil.parser.parse(row.pop('Start Date'))
    endTime = dateutil.parser.parse(row.pop('End Date'))

    events.append(PyEvent((startTime, endTime), row))

print "Imagine a person with a course schedule of 5 courses (5 randomly selected courses)."

courses = []
for i in range(0, 5):
    while True:
        n = randrange(0, len(events)-1) # get random number in csv courses list
        e = events[n]
        weekDays = getWeekDays(e)
        if weekDays:
            # find other labs and lectures of this course (course title, catalog number, instructor and subject need to be the same)
            courseTitle = e.get('Course Title')
            catalogNumber = e.get('Catalog Nbr')
            subject = e.get('Subject')
            instructor = e.get('Instructor')

            classesForCourse = []
            counter = 0
            for event in events:
                if event.get('Course Title') == courseTitle and event.get('Catalog Nbr') == catalogNumber and event.get('Subject') == subject and event.get('Instructor') == instructor:
                    wd = getWeekDays(event)
                    if wd:
                        event.set('weekDays', wd)
                        hours = getHours(event.get('Time'))
                        print hours
                        event.set('hours', hours)
                        event.set('counter', counter)
                        classesForCourse.append(event)
                    else:
                        # this class has no weekdays, find another course
                        continue
                counter += 1

            courses.append(classesForCourse)
            break

print "This person attends the following 5 courses: \n"

counter = 0
for c in courses:
    print 'Course ', counter
    print '\n'
    counter2 = 0
    for cl in c:
        print 'Class ', counter2
        print 'Week Days: ', cl.get('weekDays')
        print 'Hours: ', cl.get('hours')
        print 'Counter: ', cl.get('counter')
        counter2 += 1
        print '\n'
    counter += 1


print "Does any of these courses overlap with another course?"

overlapping = False
counter = 1

# loop over every class of every course
for x in range(0, len(courses)):
    for y in range(0, len(courses[x])):
        mycourse = courses[x][y]
        mycourseWeekDays = mycourse.get('weekDays')
        mycourseHours = mycourse.get('hours')

        for v in range(x, len(courses)):
            start = 0
            if v == x:
                if len(courses[x]) - 1 > y:
                    start = y + 1
                else:
                    continue
            for w in range(start, len(courses[v])):
                cl = courses[v][w]

                if cl.overlap(mycourse) or cl.during(mycourse) or mycourse.overlap(cl) or mycourse.during(cl):
                    startDate = mycourse.when() if cl.before(mycourse) else cl.when()
                    startDateWeekDay = startDate.weekday()
                    endDate = cl.when() if cl.before(mycourse) else mycourse.when()

                    wd = startDate.weekday()
                    mutualWeekDays = list((set(mycourseWeekDays)) & set(cl.get('weekDays')))

                    if mutualWeekDays:
                        for m in mutualWeekDays:
                            dayDifference = 0
                            if startDateWeekDay <= m:
                                dayDifference = m - startDateWeekDay
                            else:
                                dayDifference = 7 + m - startDateWeekDay

                            classDate = startDate + timedelta(days=dayDifference)

                            if classDate <= endDate:
                                #overlap function
                                classHours = cl.get('hours')
                                if ((mycourseHours[0] <= classHours[0] < mycourseHours[1]) or (classHours[0] <= mycourseHours[0] < classHours[1])) and (mycourse.get('Course Title') != cl.get('Course Title') or mycourse.get('Catalog Nbr') != cl.get('Catalog Nbr')):
                                    if overlapping is False:
                                        print "Yes, there are the following overlaps: \n"
                                        overlapping = True

                                    print "Overlap " + str(counter) + ": \n"

                                    print "Class: " + cl.get('Catalog Nbr') + ' ' + cl.get('Course Title')
                                    print "Subject: " + cl.get('Subject')
                                    print "Time: " + getWeekDayName(m) + ", " + cl.get('Time')

                                    print "\nOverlaps with: \n"

                                    print "Class: " + mycourse.get('Catalog Nbr') + ' ' + mycourse.get('Course Title')
                                    print "Subject: " + mycourse.get('Subject')
                                    print "Time: " + getWeekDayName(m) + ", " + mycourse.get('Time') + "\n"

                                    counter += 1

if overlapping is False:
    print "None of the courses overlaps with another course\n"

print "What is the next time and date for a certain course?"

# random course
l = randrange(0, len(courses)-1)
m = 0
if len(courses[l]) > 1:
    m = randrange(0, len(courses[l])-1)

randomCourse = courses[l][m]

period = randomCourse.within()
startTime = randomCourse.get("hours")[0]

wds = randomCourse.get("weekDays")

# set a make-up date
currentDatetime = datetime(2014, 1, 21, 11, 26, 0)
currentWeekDay = currentDatetime.weekday()
courseStarttime = datetime.combine(date(currentDatetime.year, currentDatetime.month, currentDatetime.day), startTime)

# get the number of days up to the next class
closestDayDifference = 7
for d in wds:
    dayDifference = 0
    if currentWeekDay <= d:
        dayDifference = d - currentWeekDay
    else:
        dayDifference = 7 + d - currentWeekDay

    if dayDifference < closestDayDifference:
        if not (dayDifference == 0 and courseStarttime < currentDatetime):
            closestDayDifference = dayDifference

# day of next class
nextCourseDay = currentDatetime + timedelta(days=closestDayDifference)

#check if it is within the course period
if period[0] <= nextCourseDay <= period[1]:
    print "The next date and time for the course" + randomCourse.get('Catalog Nbr') + ' ' + randomCourse.get('Course Title') + " is:"
    print str(nextCourseDay.month) + "/" + str(nextCourseDay.day) + "/" + str(nextCourseDay.year) + " " + str(randomCourse.get('Time'))
else:
    print "There are no classes for that course anymore"

print "Which courses are before that course on the same day?"

print "Which courses are after that course on the same day?"



