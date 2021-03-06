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




developerFreqList = []

for child in resolution_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList and child.get('id') in Bug.fixedBugIds:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)



for child in resolution_core_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_core_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList and child.get('id') in Bug.fixedBugIds:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)



for child in resolution_firefox_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_firefox_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList and child.get('id') in Bug.fixedBugIds:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)




for child in resolution_thunder_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED" and child.get('id') in Bug.fixedBugIds:
        bug = Bug(child.get('id'))

for child in assigned_to_thunder_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child[len(child.getchildren()) - 1][1].text not in Developer.developerList:
            developerFreqList.append(child[len(child.getchildren()) - 1][1].text)
        dev = Developer(child[len(child.getchildren()) - 1][1].text)



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