# About
This folder contains structures solutions and reference for the exercises contained on [bandit.overthewire](https://overthewire.org/wargames/).

Documented answers to the non-trivial questions can be found below, and all the passwords are available in the workspace file, and more detailed solutions can be read in the answers.md file.

## Level 6
#### Learning outcome: Using find to filter by file type.
Here we are looking for a file with the properties:
- human-readable
- 1033 bytes in size
- not executable

The following command therefore means "search the root directory for anything owned by user bandit7 and group bandit6 that is 33 bytes in size.

```find / ```


## Level 7
#### Learning outcome: Using find to filter by file type.
Here we are looking for a file with the properties:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

The following command therefore means "search the root directory for anything owned by user bandit7 and group bandit6 that is 33 bytes in size.

```find / -user bandit7 -group bandit6 -size 33c```

## Level 9
#### Learning outcome: Using sort and uniq.
`sort data.txt | uniq -u`

## Level 10
#### Learning outcome: Text search with grep
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