# Use the XML DOM to parse a document in memory

import xml.dom.minidom
import requests


def main():
    # retrieve the XML data using the requests library
    url = "http://httpbin.org/xml"
    result = requests.get(url)
    
    # TODO: parse the returned content into a DOM structure

    # TODO: display some information about the content

    # manipulate the XML content in memory
    # TODO: create a new item tag

    # TODO: add some text to the item

    # TODO: now add the item to the first slide

    # TODO: Now count the item tags again
    

if __name__ == "__main__":
    main()
