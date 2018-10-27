import xml.etree.ElementTree as ET
import csv



files = []
files.append("short_desc_bugzilla.xml")
files.append("short_desc_core.xml")
files.append("short_desc_firefox.xml")
files.append("short_desc_thunder.xml")

Resident_data = open('ResidentData.csv', 'w')

csvwriter = csv.writer(Resident_data)
resident_head = []

count = 0
line = 0 

for i in range(4):
    tree = ET.parse(files[i])
    root = tree.getroot()

    for member in root.findall('report'):
        if count == 0:
            id_tag = member.tag
            resident_head.append(id_tag)
            tag = member[0].tag
            resident_head.append(tag)
            csvwriter.writerow(resident_head)
            count = count + 1
        report = []
        report_id = member.attrib
        report.append(report_id)
        #what = member[0][1].text
        #report.append(what)

        what = ""

        for update in member.findall('update'):
            what = what + " " + str(update[1].text)

        if what != "":    
            report.append(what)
            csvwriter.writerow(report)

        line = line + 1
        #if line > 65000:
        #   break;


    

Resident_data.close()