![CodeQL](https://github.com/RJColeman/tools/workflows/CodeQL/badge.svg)
> :warning: :warning: WARNING :warning: :warning: As with any and all hacking or penetration testing tools, these should never be used against sites, networks, or technology you do not own and do not have express premission to run them against. If run against entities for which you do not have documented permission to attack, you could face criminal charges. 

# Licensing

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Tools

## osint/findDefaultPages.py 

Python3 script that accepts a file as input which should contain one IP address or one URL per line

For each line in the provided file, this script will:

1. attempt to access http://[ip or url] and https://[ip or url]
2. pull down content found at http://[ip or url] and https://[ip or url]
3. check if content matches known default server web pages
4. if page not found or content matches, prints tab delimited output detailing findings 

To use the script:
```
usage: python findDefaultPages.py -h or python findDefaultPages.py -f [file]

     -h --help:     display help info
     -r --reverse:  only print URLs or IP addresses where content was found but not default webserver pages
     -f --file:     path to file containing urls or ip addresses to query for default webserver pages
```
## attack/createAttack.py

> NOTE: This is a work in progress. It's usable but needs improvement to be more friendly.

Python3 script that generates the beginning of an attack script against the url provided. The script uses attack.py.tmpl, replacing variables in the tmpl file with values provided in call to createAttack.py. Once script is created, user should open new script and complete the attack code as outlined in the new script. 

The benefit of using createAttack.py is import statements are written, url request code is written, among other things. User doesn't need to write from scratch.

```
usage: createAttack.py -h
       createAttack.py -u [url] -s [scriptname.py]

options:

    -h --help:     display help info

    -s --script:   required name of script to create
    -u --url:      required url of target site or page ie www.somesite.com
    -p --protocol: protocol ie http, ftp, https
    -o --port:     port ie 80, 443, 8080
    -g --page:     page to hit on the site ie "path/to/page.php
    -c --cookie:   cookie value ie PHPSESSID=XXX999XXX
    -a --auth:     value of Authorization header
    -t --agent:    value of User-Agent header; default is:

    Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0

Example usage creates a scipt called attack.py:

     createAttack.py -u 'www.someurl.com' \
                     -p 'http'  \
                     -g 'path/to/page.php'  \
                     -a 'Basic bmSomeBasicAuthStringGoesHere9999XXXXXN0TlZrbXhkazM5Sg==' \
                     -s attack.py

     createAttack.py --url 'www.someurl.com' \
                     --protocol 'http'  \
                     --page 'path/to/page.php'  \
                     --auth 'Basic bmSomeBasicAuthStringGoesHere9999XXXXXN0TlZrbXhkazM5Sg==' \
                     --script attack.py


```
