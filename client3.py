import requests
url="http://127.0.0.1:9090/version"
cookies={"_intern":"harrish"}
r=requests.get(url=url,allow_redirects=False,cookies=cookies)

print("Response Headers: ",r.headers,"\n")
print("\nResponse code: ",r.status_code)
print("\nData :",r.text)
print("\nCookies: ",r.cookies)



