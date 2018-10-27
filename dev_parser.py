import xml.etree.ElementTree as ET
import csv

class Developer:
   devCount = 0
   devList = []
   def __init__(self, name):
        self.name = name
        Developer.devCount += 1
        Developer.devList.append(self)


class Bug:
    fixedBugIds = []
    def __init__(self, bugId, status):
        self.bugId = bugId
        self.status = status
        if status == "FIXED":
            Bug.fixedBugIds.append(self)
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


for child in resolution_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'), 'FIXED')

for child in resolution_core_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'), 'FIXED')

for child in resolution_firefox_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'), 'FIXED')

for child in resolution_thunder_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'), 'FIXED')


Bug_data = open('BugIds.csv', 'w')

csvwriter = csv.writer(Bug_data)
Bug_head = []

Bug_head.append('Id')
Bug_head.append('Status')
csvwriter.writerow(Bug_head)


Developer_data = open('Developers.csv', 'w')
csvwriter = csv.writer(Developer_data)
Dev_head = []

Dev_head.append('developer')
csvwriter.writerow(Dev_head)


for child in assigned_to_bugzilla_root:
    if child[len(child.getchildren()) - 1][1].text:
        dev_row = []
        dev_row.append(child[len(child.getchildren()) - 1][1].text)
        csvwriter.writerow(dev_row)

for child in assigned_to_core_root:
    if child[len(child.getchildren()) - 1][1].text:
        dev_row = []
        dev_row.append(child[len(child.getchildren()) - 1][1].text)
        csvwriter.writerow(dev_row)

for child in assigned_to_firefox_root:
    if child[len(child.getchildren()) - 1][1].text:
        dev_row = []
        dev_row.append(child[len(child.getchildren()) - 1][1].text)
        csvwriter.writerow(dev_row)

for child in assigned_to_thunder_root:
    if child[len(child.getchildren()) - 1][1].text:
        if child.get('id') in Bug.fixedBugIds
            dev_row = []
            dev_row.append(child[len(child.getchildren()) - 1][1].text)
            csvwriter.writerow(dev_row)

Developer_data.close()

import pandas as pd


developerList = []
with open('Developers.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row not in developerList:
            developerList.append(row['developer'])


for member in Bug.fixedBugIds:
    Bug_row = []
    bug_id = member.bugId
    Bug_row.append(bug_id)
    bug_status = member.status
    Bug_row.append(bug_status)
    csvwriter.writerow(Bug_row)

Bug_data.close()







for member in Bug.fixedBugIds:
    ass_child = assigned_to_bugzilla_root.find(".//*[@id='%s']" %member.bugId)
    if ass_child[len(ass_child.getchildren()) - 1][1].text:
        if ass_child[len(ass_child.getchildren()) - 1][1].text not in developerList:
            developerList.append(ass_child[len(ass_child.getchildren()) - 1][1].text)

developerList.clear()

for member in Bug.fixedBugIds:
    ass_child = assigned_to_bugzilla_root.find(".//*[@id='%s']" %member.bugId)
    if ass_child != '' and ass_child not in developerList:
        developerList.append(ass_child)

