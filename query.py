import requests
import sys

query = sys.argv[1]
response = requests.post(f'http://10.29.4.48:30944/qa/?query={query}')
print(response.content.decode())
