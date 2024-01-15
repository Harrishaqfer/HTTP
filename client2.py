import requests
url="http://127.0.0.1:9090/version"
responses=requests.get(url,allow_redirects=False)
print("\nstatus code:",responses.status_code)
print("response headers:")
for a in responses.headers:
    print(a,":",responses.headers[a])