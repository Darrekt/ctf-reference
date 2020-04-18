# About
This folder contains structures solutions and reference for the exercises contained on [natas.overthewire](https://overthewire.org/wargames/natas/).
Documented answers to the non-trivial questions can be found below, and all the passwords are available in the workspace file, and more detailed solutions can be read in the answers.md file.

# Key Learning Takeaways


# Solutions
## Level 0 - 1
Simple: just inspect the html source of the page and the password is in a comment.

## Level 1 - 2
Same: right clicking still works, but even if it doesn't you can use your browser's developer tools (F12).

## Level 2 - 3
A new <img> is available in the source code. We see that it is in a relative directory, so maybe we can find something by looking in that same folder that the image is in. 

This hints us to a Path Traversal attack. Browsing to /files reveals that there is a users.txt file, which contains our password.


## Level 3 - 4
The hint is that Google can't even find the page. Therefore, we're going to look in the robots.txt file. We see here that the /s3cr3t directory has been disallowed from crawl traversal. Looking in to it reveals the password file.


## Level 4 - 5
The page tells us that we are not allowed to access this resource from natas4, so we need to set up a HTTP debug proxy to spoof our referer to "http://natas5.natas.labs.overthewire.org/". We can do this with Burp suite. Simply change the Referer header in the HTTP request and we are in with the password.

## Level 5 - 6
The page tells us that we are not logged in. Thankfully, our HTTP proxy that we set up tells us that the cookie loggedin has a value of 0. Assuming this is boolean value, let's change it to 1. As expected, it works and we get the password.

## Level 6 - 7
Inspecting the PHP code for the site reveals that the secret is contained in includes/secret.inc, so a path traversal will get us the password.

## Level 7 - 8
We've got a helpful hint in the comments here that the pasword is in `/etc/natas_webpass/natas8`. We also see that the pages are nagivated using the query string. Trying a random query string such as "hello" gives us a rather helpful error:

```php
Warning: include(hello): failed to open stream: No such file or directory in /var/www/natas/natas7/index.php on line 21
```

This also leads us to believe the output of the PHP file is printed directly to HTML. So, we can just change the query string to "?page=../../../../../etc/natas_webpass/natas8", which should navigate us to the desired file.

## Level 8 - 9
The PHP source code reveals the encoding of the secret, so this is a bit of a no-brainer. We don't have a limit on the length of input either, so let's just find out the relevant PHP functions to reverse-engineer our code. We can reverse engineer the password using our own PHP interactive shell:

```
darrick@Desktop-SG:~/Desktop/Work/Cyber-security/ctf-reference$ php -a
Interactive mode enabled

php > echo base64_decode(strrev(hex2bin("3d3d516343746d4d6d6c315669563362")));
oubWYf2kBq
```
Now that we know the secret, getting the password is easy.

TODO: Find out why trying to execute the code directly in the form submission doesn't work.

## Level 9 - 10
Inspecting the PHP code, we see that there is a line where the query string gets used in a passthrough shell command:
```php
if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
```

Since the query string goes through no prior checks, we can exploit the passthrough command using an untrusted query string attack: `; cat /etc/natas_webpass/natas10;`.

Semantically, this escapes the grep command, then prints our desired file to output. The final semicolon stops the entire dictionary from being printed as part of the `cat` command.
