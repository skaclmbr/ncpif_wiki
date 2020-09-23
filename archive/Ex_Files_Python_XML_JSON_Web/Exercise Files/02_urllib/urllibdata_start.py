# Send data to a server using urllib

# TODO: import the request and parse modules
import urllib.request


def main():
    url = "http://httpbin.org/get"

    # TODO: create some data to pass to the GET request


    # TODO: the data needs to be url-encoded before passing as arguments


    # TODO: issue the request with the data params as part of the URL
    result = urllib.request.urlopen(url)

    # TODO: issue the request with a data parameter to use POST
   
    print("Result code: {0}".format(result.status))
    print("Returned data: ----------------------")
    print(result.read().decode("utf-8"))


if __name__ == "__main__":
    main()
