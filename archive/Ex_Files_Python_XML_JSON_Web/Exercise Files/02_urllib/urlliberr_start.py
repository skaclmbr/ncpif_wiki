# handling errors and status codes

# TODO: import the request, error, and status modules
import urllib.request


def main():
    #url = "http://no-such-server.org"      # will generate a URLError
    #url = "http://httpbin.org/status/404"  # will generate an HTTPError
    url = "http://httpbin.org/html"         # should work with no errors

    # TODO: use exception handling to attempt the URL access
    result = urllib.request.urlopen(url)
    print("Result code: {0}".format(result.status))
    if (result.getcode() == 200):
        print(result.read().decode('utf-8'))

if __name__ == "__main__":
    main()

