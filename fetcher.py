# Legis.xml has a structure with the following child Regulation to the root node:
# - LinkToXML
# - Title
# Open the file and find all nodes that have a Title containing the word food or aliment
# Print the Title and the LinkToXML for each node found
# Hint: use the findall method to find all nodes that have a Title containing the word food or aliment
# Hint: use the get method to get the value of the attribute LinkToXML
# Then fetch and cache the file locally for LinkToXML

# use lxml to parse the XML file
# import the library to parse XML
import os
import re
import time
import lxml.etree as ET

# import the library to parse XML
# import xml.etree.ElementTree as ET


# import the library to fetch the file from the web
import urllib.request, urllib.parse, urllib.error

# import the library to ignore SSL certificate errors
import ssl

# import the library to read all XML files from data/ subdirectory
import glob

# import the library to strip all tags
import re

# import the library to format text
import textwrap

def fetch_acts():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # load XML file Legis.xml
    url = 'https://laws-lois.justice.gc.ca/eng/XML/Legis.xml'
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read()
    tree = ET.fromstring(data)

    lst = tree.findall(".//Act")

    lastTime = time.time()
    for item in lst:
        title = item.find('Title').text
        # if re.search('food|aliment|insect|insectes|plant|volaille|poultry|import|health|hygiène|santé', title, re.IGNORECASE) :
        if True:
            print(title)
            # fetch and cache the file locally for LinkToXML
            url = item.find('LinkToXML').text
            fname = 'data/acts/' + url.split('/')[-1]
            if os.path.isfile(fname):
                print('Already retrieved', fname)
                continue
            print('Retrieving', url)
            # wait for at least 1 second from last request sent
            # get current time in seconds
            remaining = lastTime + 1 - time.time()
            if remaining > 0:
                time.sleep(remaining)
            lastTime = time.time()
            uh = urllib.request.urlopen(url, context=ctx)
            data = uh.read()
            print('Retrieved', len(data), 'characters')
            # save the file locally
            with open(fname, 'w') as fhand:
                fhand.write(data.decode())
            print('Saved', fname)
            
        print(title)


if __name__ == '__main__':
    fetch_acts()
