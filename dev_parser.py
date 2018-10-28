import xml.etree.ElementTree as ET
import csv

class Developer:
   devCount = 0
   developerList = []
   def __init__(self, name, id):
        self.name = name
        self.id = id
        Developer.devCount += 1
        Developer.developerList.append(self)


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
    if child[len(child.getchildren()) - 1][1].text and child.get('id') in Bug.fixedBugIds:
        dev = Developer(child[len(child.getchildren()) - 1][1].text, child.get('id'))

for child in short_desc_bugzilla_root:
    report_id = child.get('id')
    if report_id in Bug.fixedBugIds:
        what = ""
        for update in child.findall('update'):
            what = what + " " + str(update[1].text)
        if what != "":    
            for lep in Developer.developerList:
                if(lep.id == report_id):
                    report = Report(report_id, what, lep.name)
        





for child in resolution_core_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_core_root:
    if child[len(child.getchildren()) - 1][1].text and child.get('id') in Bug.fixedBugIds:
        dev = Developer(child[len(child.getchildren()) - 1][1].text, child.get('id'))

for child in short_desc_core_root:
    report_id = child.get('id')
    if report_id in Bug.fixedBugIds:
        what = ""
        for update in child.findall('update'):
            what = what + " " + str(update[1].text)
        if what != "":    
            for lep in Developer.developerList:
                if(lep.id == report_id):
                    report = Report(report_id, what, lep.name)



for child in resolution_firefox_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_firefox_root:
    if child[len(child.getchildren()) - 1][1].text and child.get('id') in Bug.fixedBugIds:
        dev = Developer(child[len(child.getchildren()) - 1][1].text, child.get('id'))

for child in short_desc_firefox_root:
    report_id = child.get('id')
    if report_id in Bug.fixedBugIds:
        what = ""
        for update in child.findall('update'):
            what = what + " " + str(update[1].text)
        if what != "":    
            for lep in Developer.developerList:
                if(lep.id == report_id):
                    report = Report(report_id, what, lep.name)




for child in resolution_thunder_root:
    if child[len(child.getchildren()) - 1][1].text == "FIXED":
        bug = Bug(child.get('id'))

for child in assigned_to_thunder_root:
    if child[len(child.getchildren()) - 1][1].text and child.get('id') in Bug.fixedBugIds:
        dev = Developer(child[len(child.getchildren()) - 1][1].text, child.get('id'))

for child in short_desc_thunder_root:
    report_id = child.get('id')
    if report_id in Bug.fixedBugIds:
        what = ""
        for update in child.findall('update'):
            what = what + " " + str(update[1].text)
        if what != "":    
            for lep in Developer.developerList:
                if(lep.id == report_id):
                    report = Report(report_id, what, lep.name)




Report_data = open('Report.csv', 'w')

csvwriter = csv.writer(Report_data)
Report_head = []
Report_head.append('id')
Report_head.append('short_desc')
Report_head.append('developer')
csvwriter.writerow(Report_head)

for report in Report.reports:
    report_row = []
    report_row.append(report.bugId)
    report_row.append(report.shortDesc)
    report_row.append(report.developer)
    csvwriter.writerow(report_row)

Report_data.close()