import glob
import re
import lxml.etree as ET
import os

# format XML with indentation
from bs4 import BeautifulSoup

def HTMLEntitiesToUnicode(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    text = str(BeautifulSoup(text, features="xml"))
    return text

def totext(xml):
    data = ET.tostring(xml, pretty_print=True)
    data = HTMLEntitiesToUnicode(data)
    # strip all tags
    data = re.sub('<[^>]*>', '', data)
    # remove empty lines in data
    data = os.linesep.join([s for s in data.splitlines() if s])
    return data

def chunk():
    # read all XML files from data/ subdirectory
    files = glob.glob('data/acts/*.xml')
    for file in files:
        # open the file
        print(file)
        with open(file, 'r') as fhand:
            # read the file
            data = fhand.read()
            data = ET.fromstring(data)
            # extract ConsolidatedNiumber
            consolidatedNumber = data.find(".//ConsolidatedNumber").text
            print(consolidatedNumber)
            xRefs = data.findall(".//XRefExternal")
            if not xRefs:
                print('Skipping', consolidatedNumber)
                continue
            xrefExternal = xRefs[0].text
            act_dir = 'data/sections/' + consolidatedNumber
            os.makedirs(act_dir, exist_ok=True)
            # iterate through all child nodes of Body
            for section in data.findall(".//Body/Section"):
                # print(ET.tostring(section, pretty_print=True).decode())
                if len(section.findall('.//Repealed')) > 0:
                    print('Skipping repealed section of', consolidatedNumber)
                    continue
                
                label = section.findall('./Label')[0]
                labelText = label.text if label.text else 'OTHER'
                label.getparent().remove(label)
                content = totext(section)
                content = f"{xrefExternal}\nAct {consolidatedNumber}\nSection {labelText}\n{content}"
                fname = act_dir + '/' + labelText + '.txt'
                with open(fname, 'w+') as fhand:
                    fhand.write(content)


if __name__ == '__main__':
    chunk()