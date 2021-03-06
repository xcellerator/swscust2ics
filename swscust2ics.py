#!/usr/bin/python
from ics import Calendar, Event
from pathlib import Path
from collections import namedtuple
import pandas as pd
import sys
import arrow

# Set up TimeTableEntry data structure
TimeTableEntry = namedtuple("TimeTableEntry", "Day Start End Description Type Room Staff Dates")

def checkArgs():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " input.html output.ics")
        exit()
    else:
        checkExists(sys.argv[1])

def checkExists(filename):
    file = Path(filename)
    if file.is_file():
        pass
    else:
        print("ERROR: " + filename + " doesn't exist!")
        exit()

# Write the ICS structure to a file
def exportCalendarICS(filename, calendar):
    with open(filename, 'w') as f:
        f.writelines(calendar)

# Open the HTML file as a string
def importCalendarHTML(filename):
    with open(filename, 'r') as inputfile:
        data = inputfile.read()
    return data

# Add a new event to the TimeTable
def AddTimeTableEvent(tt, day, start, end, desc, type, room, staff, dates):
    tt.append(TimeTableEntry(day, start, end, desc, type, room, staff, dates))

# Split the raw HTML into tables via each day
def ParseDays():
    raw_html = importCalendarHTML(sys.argv[1])
    Days = []
    for i in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        try:
            Days.append(pd.read_html(raw_html, header=0, match=i))
        except:
            continue
    return Days

# Pull out each entry from a table to and compile an entry
def BuildTimeTable(Days):
    TimeTable = []
    for i in range(len(Days)):
        for j in range(len(Days[i])):
            for k in range(len(Days[i][j])):
                day = Days[i][j].get("Day")[k]
                start = Days[i][j].get("Start")[k]
                end = Days[i][j].get("End")[k]
                desc = Days[i][j].get("Description")[k]
                type = Days[i][j].get("Type")[k]
                room = Days[i][j].get("Room")[k]
                staff = Days[i][j].get("Staff")[k]
                dates = Days[i][j].get("Activity Date(s)")[k]
                dates = dates.split(";")
                AddTimeTableEvent(TimeTable, day, start, end, desc, type, room, staff, dates)
    return TimeTable

# Convert the date into one accepted by Arrow
def FormatDate(date):
    array = date.split("/")
    year = "20" + str(array[2])
    month = array[1]
    day = array[0]
    new_date = year + "-" + month + "-" + day
    return new_date

# Convert the time into one accepted by Arrow
def FormatTime(time):
    array = time.split(":")
    if len(array[0]) == 1:
        array[0] = "0" + array[0]
    time = array[0] + ":" + array[1]
    return time

# Generate an Arrow datetime string
def GenerateArrow(date, time):
    string = FormatDate(date) + " " + FormatTime(time) + ":00"
    string = arrow.get(string, 'YYYY-MM-DD HH:mm:ss')
    if string.month in [4,5,6,7,8,9,10]:
        string = string.replace(hour=(string.hour-1))
    return string

def GetDuration(start, end):
    diff = end - start
    return diff

# Construct a calendar from the TimeTable structure
def BuildCalendar(TimeTable):
    c = Calendar()
    for i in range(len(TimeTable)):
        entry = TimeTable[i]
        for j in range(len(entry.Dates)):
            e = Event()
            date = entry.Dates[j]
            start = entry.Start
            end = entry.End
            e.name = str(entry.Description + " (" + entry.Type + ")")
            e.begin = GenerateArrow(date, start)
            e.duration = GenerateArrow(date, end) - GenerateArrow(date, start)
            e.location = str(entry.Room)
            e.description = str(entry.Staff)
            c.events.add(e)
    return c

# Spit out the ICS
def OutputICS(Calendar):
    with open(sys.argv[2], 'w') as output:
        output.writelines(Calendar)

########################################################################
# Do the thing
# Check we have enough arguments
checkArgs()

# Break the table up into each day
Days = ParseDays()

# Construct the TimeTable object from the data parsed from the table
TimeTable = BuildTimeTable(Days)

# Build the calendar from the TimeTable
Calendar = BuildCalendar(TimeTable)

# Write to file
OutputICS(Calendar)
