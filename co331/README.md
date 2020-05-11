# CO331 Networks and Web Security
This document archives some of the key learning points I took away from the module at Imperial College, courtesy of the Department of Computing.

## Attacks

### Passwords

#### Offline Dictionary Attack [I]
Conditions:
- Obtain password file of hashed passwords

Procedure:
- Build Rainbow tables (dictionaries) of hashes based off popular passwords or wordlists
- If you find a match in the password file, you've cracked a password for that user.

Tools:
- John the Ripper

Countermeasures:
- Use dedicated hashing functions to make building rainbow tables slow
- Salted hashes to prevent dictionary attacks on the whole userbase
- 2FA, hardware tokens, notifying users on login, etc.


#### Online Dictionary Attack
Conditions:
- 

Procedure:
1. 

Tools:
- 

### DNS

#### DNS MITM / Hijacking Attack
Conditions:
- Either own a DNS server
- Or compromise it to your own benefit

Procedure:
1. Change the name server entry to a malicious IP of your choice
2. To avoid suspicion, give honest answers to everyone except your shortlisted IPs?

Examples:
- DNSpionage

#### DNS Cache Poisoning
Conditions:
- Off-path or MITM capabilities

Procedure:
1. (MITM) Intercept the DNS packet in transit and change the value IP mapping
2. (Off-path) Race to spoof a DNS reply before the server. It is possible to brute force all 2^16 TXIDs before the DNS replies. See Kaminsky's DNS Cache Poisining Attack.


#### DNS Tunneling
Conditions:
- Participant capabilities
