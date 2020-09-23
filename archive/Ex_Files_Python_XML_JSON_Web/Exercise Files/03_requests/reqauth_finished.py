# using the requests library to access internet data

import requests
from requests.auth import HTTPBasicAuth

def main():
    # Access a URL that requires authentication - the format of this 
    # URL is that you provide the username/password to auth against
    url = "http://httpbin.org/basic-auth/JoeMarini/MySecretWord"

    # Create a credentials object using HTTPBasicAuth
    myCreds = HTTPBasicAuth('JoeMarini', 'MySecretWord')

    # Issue the request with the authentication credentials
    result = requests.get(url, auth=myCreds)
    printResults(result)


def printResults(resData):
    print("Result code: {0}".format(resData.status_code))
    print("\n")

    print("Returned data: ----------------------")
    print(resData.text)

if __name__ == "__main__":
    main()
