# using the requests library to access internet data

#import the requests library
import requests
import json


def main():
    # Use requests to issue a standard HTTP GET request
    url = "http://httpbin.org/json"
    result = requests.get(url)

    # Use the built-in JSON function to return parsed data
    dataobj = result.json()
    print(json.dumps(dataobj,indent=4))

    # Access data in the python object
    print(list(dataobj.keys()))

    print(dataobj['slideshow']['title'])
    print("There are {0} slides".format(len(dataobj['slideshow']['slides'])))


if __name__ == "__main__":
    main()
