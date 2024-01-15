import requests
url="https://c006.preprod.aqfer.net/1/a/c.gif"
responses=requests.get(url,allow_redirects=False)
print("\nstatus code:",responses.status_code)
print("response headers:")
for a in responses.headers:
    print(a,":",responses.headers[a])