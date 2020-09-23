# Use the lxml library to parse a document in memory

import requests
from lxml import etree


def main():
    slideCount = 0
    itemCount = 0

    # retrieve the XML data using the requests library
    url = "http://httpbin.org/xml"
    result = requests.get(url)

    # build a doc structure using the ElementTree API
    doc = etree.fromstring(result.content)
    print(doc.tag)

    # Access the value of an attribute
    print(doc.attrib['title'])

    # Iterate over tags
    for elem in doc.findall('slide'):
        print (elem.tag)

    # Create a new slide
    newSlide = etree.SubElement(doc, "slide")
    newSlide.text = "This is a new slide"

    # Count the number of slides
    slideCount = len(doc.findall("slide"))
    itemCount = len(doc.findall(".//item"))

    print("There were {0} slide elements".format(slideCount))
    print("There were {0} item elements".format(itemCount))


if __name__ == "__main__":
    main()
