import xml.etree.ElementTree as ET
import csv

class Developer:
   devCount = 0
   developerList = []
   def __init__(self, name):
        self.name = name
        Developer.devCount += 1
        Developer.developerList.append(name)


class Bug:
    fixedBugIds = []
    def __init__(self, bugId):
        self.bugId = bugId
        Bug.fixedBugIds.append(bugId)



class Report:
    reports = []
    def __init__(self, bugId, shortDesc, developer):
        self.bugId = bugId
        self.shortDesc = shortDesc
        self.developer = developer
        Report.reports.append(self)


##
#assign to xmls
##
assigned_to_bugzilla = ET.parse('developers/assigned_to_bugzilla.xml')
assigned_to_bugzilla_root = assigned_to_bugzilla.getroot()

assigned_to_core = ET.parse('developers/assigned_to_core.xml')
assigned_to_core_root = assigned_to_core.getroot()

assigned_to_firefox = ET.parse('developers/assigned_to_firefox.xml')
assigned_to_firefox_root = assigned_to_firefox.getroot()

assigned_to_thunder = ET.parse('developers/assigned_to_thunder.xml')
assigned_to_thunder_root = assigned_to_thunder.getroot()

##
#resolution xmls
##
resolution_bugzilla = ET.parse('resolution/resolution_bugzilla.xml')
resolution_bugzilla_root = resolution_bugzilla.getroot()

resolution_core = ET.parse('resolution/resolution_core.xml')
resolution_core_root = resolution_core.getroot()

resolution_firefox = ET.parse('resolution/resolution_firefox.xml')
resolution_firefox_root = resolution_firefox.getroot()

resolution_thunder = ET.parse('resolution/resolution_thunder.xml')
resolution_thunder_root = resolution_thunder.getroot()



##
#short_desc xmls
##
short_desc_bugzilla = ET.parse('short_desc/short_desc_bugzilla.xml')
short_desc_bugzilla_root = short_desc_bugzilla.getroot()

short_desc_core = ET.parse('short_desc/short_desc_core.xml')
short_desc_core_root = short_desc_core.getroot()

short_desc_firefox = ET.parse('short_desc/short_desc_firefox.xml')
short_desc_firefox_root = short_desc_firefox.getroot()

short_desc_thunder = ET.parse('short_desc/short_desc_thunder.xml')
short_desc_thunder_root = short_desc_thunder.getroot()






developerFreqList = []

for child in resolution_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)



for child in resolution_core_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_core_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)



for child in resolution_firefox_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_firefox_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)




for child in resolution_thunder_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_thunder_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)

BugId_data = open('BugId.csv', 'w')

csvwriter = csv.writer(BugId_data)
BugId_head = []
BugId_head.append('id')
csvwriter.writerow(BugId_head)

for bug in Bug.fixedBugIds:
    BugId_row = []
    BugId_row.append(bug)
    csvwriter.writerow(BugId_row)

BugId_data.close()

Developer_data = open('Developers.csv', 'w')

csvwriter = csv.writer(Developer_data)
Developer_head = []
Developer_head.append('developer')
Developer_head.append('Num of Bugs')
csvwriter.writerow(Developer_head)

for i in range(len(developerFreqList)):
    Developer_row = []
    Developer_row.append(developerFreqList[i])
    Developer_row.append(Developer.developerList.count(developerFreqList[i]))
    csvwriter.writerow(Developer_row)

Developer_data.close()