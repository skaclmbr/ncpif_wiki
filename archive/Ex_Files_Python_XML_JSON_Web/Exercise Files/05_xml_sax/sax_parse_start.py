# parse XML data using the SAX parser

import requests
import xml.sax

# TODO: define the ContentHandler subclass for our content
class MyContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.slideCount = 0
        self.itemCount = 0

    #TODO: Handle startElement

    #TODO: Handle endElement

    #TODO: Handle text data

    #TODO: Handle startDocument

    #TODO: Handle endDocument


def main():
    # create a new content handler for the SAX parser
    handler = MyContentHandler()

    # use the Requests lib to get XML data from the server
    # remember that Requests auto-decodes our content
    url = "http://httpbin.org/xml"
    result = requests.get(url)

    # TODO: call the parseString method on the XML text content received
    

    # when we're done, print out some interesting results
    print("There were {0} slide elements".format(handler.slideCount))
    print("There were {0} item elements".format(handler.itemCount))


if __name__ == "__main__":
    main()
