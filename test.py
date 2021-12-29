import requests

print(requests.Session().head("url",allow_redirects=True).url)