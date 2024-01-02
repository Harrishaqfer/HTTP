import requests

def make_get_request(url):
    try:
        # Send a GET request
        response = requests.get(url)

        # Print the status code
        print(f"Status Code: {response.status_code}")

        # Print the response headers
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")

    except requests.RequestException as e:
        print(f"Error making GET request: {e}")

# Replace "https://example.com" with the actual URL you want to make a GET request to
url = "https://c006.preprod.aqfer.net/1/a/c.gif"
make_get_request(url)
