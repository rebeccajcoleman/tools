#!/usr/bin/python
import fileinput
from shutil import copyfile
import getopt, sys
import re
import os

protocol = 'http' 
url = None
port = '' 
page = ''

cookie =  ''
auth = '' 
user_agent = ''
verbose = '' 

script = None

# uses command line options to set global variables
def setOpts():
    global protocol, url, port, page, cookie, auth, script, user_agent
    flags = "vhp:u:o:c:a:s:g:t:"
    longflags = ["help", "protocol=", "url=", "port=", "cookie=", "auth=", "script=", "page=", "agent="]
    try:
        opts, args = getopt.getopt(sys.argv[1:], flags, longflags)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    optsSet = True
    for o, a in opts:
        # verbose is not currently in use
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-g", "--page"):
            page = a
        elif o in ("-p", "--protocol"):
            if a not in ('ftp', 'http', 'https'):
                print("Invalid protocol. Valid values are ftp, http, https.")
                optsSet = False
            else:
                protocol = a
        elif o in ("-u", "--url"):
            url = a
            if re.match(r'^[.a-zA-Z0-9]+$', url) is None:
                print('Malformed url: ' + str(url))
                optsSet = False
        elif o in ("-o", "--port"):
            port = a
            if re.match(r'^[0-9]+$', port) is None:
                print('Invalid port: ' + port)
                optsSet = False
        elif o in ("-c", "--cookie"):
            cookie = a
            if re.match(r'^[\s;:=a-zA-Z0-9]+$', cookie) is None:
                print('Malformed cookie: can contain spaces ; : = a-zA-Z0-9')
                optsSet = False
        elif o in ("-a", "--auth"):
            auth = a
            if re.match(r'^[\s;:=a-zA-Z0-9]+$', auth) is None:
                print('Malformed auth value: can contain spaces ; : = a-zA-Z0-9')
                optsSet = False
        elif o in ("-t", "--agent"):
            user_agent = a
        elif o in ("-s", "--script"):
            script = a
            if re.match(r'^[a-zA-Z0-9]+\.py$', script) is None:
                print('Malformed script name: ^[a-zA-Z0-9]+\.py$')
                optsSet = False
            if os.path.isfile(script):
                print('Cannot create  ' + str(script) + ' - already exists.')
                optsSet = False
        else:
            assert False, "unhandled option"

    if url == None or script == None:
        usage()
        print('Note: url and script are required using -u or --url and -s or --script')
        print('')
        optsSet = False

    if optsSet is False:
        sys.exit(2)

def main():
    setOpts();

    # copy attack.py template to file with requested script name 
    copyfile(os.path.dirname(os.path.realpath(__file__)) + '/attack.py.tmpl', script)

    # read each line from newly created script and replace variables
    for line in fileinput.input(script, inplace=True):

        if '%%PROTO%%' in line:
            print(line.replace('%%PROTO%%', protocol), end="")

        elif '%%URL%%' in line:
            print(line.replace('%%URL%%', url), end="")

        elif '%%PORT%%' in line:
            print(line.replace('%%PORT%%', port), end="")

        elif '%%COOKIE%%' in line:
            print(line.replace('%%COOKIE%%', cookie), end="")

        elif '%%AUTH%%' in line:
            print(line.replace('%%AUTH%%', auth), end="")

        elif '%%PAGE%%' in line:
            print(line.replace('%%PAGE%%', page), end="")

        elif '%%USER-AGENT%%' in line:
            print(line.replace('%%USER-AGENT%%', user_agent), end="")

        else:
            print(line, end="")

def usage():
    print('')
    print('usage: createAttack.py -h')
    print('       createAttack.py -u [url] -s [scriptname.py]')
    print('')
    print('     -h --help:     display help info')
    print('')
    print('     -s --script:   required name of script to create')
    print('     -u --url:      required url of target site or page ie www.somesite.com')
    print('     -p --protocol: protocol ie http, ftp, https')
    print('     -o --port:     port ie 80, 443, 8080')
    print('     -g --page:     page to hit on the site ie "path/to/page.php')
    print('     -c --cookie:   cookie value ie PHPSESSID=XXX999XXX')
    print('     -a --auth:     value of Authorization header')
    print('     -t --agent:    value of User-Agent header; default is:')
    print('')
    print('     Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0') 
    print('')
    print('Example usage creates a scipt called attack.py:') 
    print('')
    print("     createAttack.py -u 'www.someurl.com' \\")
    print("                     -p 'http'  \\")
    print("                     -g 'path/to/page.php'  \\")
    print("                     -a 'Basic bmSomeBasicAuthStringGoesHere9999XXXXXN0TlZrbXhkazM5Sg==' \\")
    print("                     -s attack.py") 
    print('')
    print("     createAttack.py --url 'www.someurl.com' \\")
    print("                     --protocol 'http'  \\")
    print("                     --page 'path/to/page.php'  \\")
    print("                     --auth 'Basic bmSomeBasicAuthStringGoesHere9999XXXXXN0TlZrbXhkazM5Sg==' \\")
    print("                     --script attack.py") 
    print('')

if __name__ == "__main__":
    main()
