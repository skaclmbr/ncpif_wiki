# Process JSON data returned from a server

# use the JSON module
import json


def main():
    # define a python ditcionary
    pythonData = {
        "sandwich": "Reuben",
        "toasted": True,
        "toppings": ["Thousand Island Dressing",
                     "Sauerkraut",
                     "Pickles"
                     ],
        "price": 8.99
    }

    # TODO: serialize to JSON using dumps

    # TODO: print the resulting JSON string
    print("JSON Data: --------")


if __name__ == "__main__":
    main()
