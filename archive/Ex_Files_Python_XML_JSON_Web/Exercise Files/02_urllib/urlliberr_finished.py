# handling errors and status codes

#import the request, error, and status modules
import urllib.request
from urllib.error import HTTPError, URLError
from http import HTTPStatus

def main():
    url = "http://no-such-server.org"      # will generate a URLError
    #url = "http://httpbin.org/status/404"  # will generate an HTTPError
    #url = "http://httpbin.org/html"         # should work with no errors

    # use exception handling to attempt the URL access
    try:
        result = urllib.request.urlopen(url)
        print("Result code: {0}".format(result.status))
        if (result.getcode() == HTTPStatus.OK):
            print(result.read())
    # occurs when the server returns a non-success error code
    except HTTPError as err:
        print("Error: {0}".format(err.code))
    # occurs when something is wrong with the URL itself
    except URLError as err:
        print("Yeah, that server is bunk. {0}".format(err.reason))

if __name__ == "__main__":
    main()

