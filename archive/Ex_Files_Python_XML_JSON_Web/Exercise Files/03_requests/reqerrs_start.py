# using the requests library to access internet data

import requests

def main():
    # Use requests to issue a standard HTTP GET request
    url = "http://httpbin.org/status/404"
    result = requests.get(url)
    printResults(result)

    

def printResults(resData):
    print("Result code: {0}".format(resData.status_code))
    print("\n")

    print("Returned data: ----------------------")
    print(resData.text)


if __name__ == "__main__":
    main()
