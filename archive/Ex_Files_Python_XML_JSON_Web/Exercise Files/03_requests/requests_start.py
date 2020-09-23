# using the requests library to access internet data

#import the requests library
import requests

def main():
    # TODO: Use requests to issue a standard HTTP GET request

    
    # TODO: Send some parameters to the URL via a GET request
    # Note that requests handles this for you, no manual encoding


    # TODO: Pass a custom header to the server

    

def printResults(resData):
    print("Result code: {0}".format(resData.status_code))
    print("\n")

    print("Headers: ----------------------")
    print(resData.headers)
    print("\n")

    print("Returned data: ----------------------")
    print(resData.content)

if __name__ == "__main__":
    main()
