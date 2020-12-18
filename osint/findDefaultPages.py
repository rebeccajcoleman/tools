import urllib.request
import urllib.parse
from socket import timeout
import getopt, sys
import os.path
from os import path

stats = {'404s' : 0,
         'Timeouts' : 0,
         'Founds' : 0,
         'Untracked' : 0,
         'Not Founds': 0}

# set list of search phrases that indicate default web pages from well known servers
terms = {
    # debian/ubuntu apache
    b'Apache2 server after installation on Debian systems' : 'Default page Found' + "\t" + 'Apache2 on Debian/Ubuntu',
    b'The initial installation of Debian/GNU Apache' : 'Default page found  ' + "\t" + 'Apache Unknown Version',
    b'Apache2 server after installation on Ubuntu systems' : 'Default page Found' + "\t" + 'Apache2 on Debian/Ubuntu',
    # fedora apache
    b'Apache HTTP Server on Fedora Core'  : 'Default page found' + "\t" + 'Outdated Apache 2.0 on Fedora',
    b'Fedora Core Test Page' : 'Default page found' + "\t" + 'Outdated Apache 2.0 on Fedora',
    # apache
    b'Apache 2 Test Page' : 'Default page found' + "\t" + 'Apache 2 running',
    b'Apache Server Status' : 'Default page found' + "\t" + 'Apache Unknown Version',
    b'Apache/2.0.* (Linux/SuSE)' : 'Default page found' + "\t" + 'Outdated Apache2.0 on Linux SuSE' ,
    b'xampp/index'  : 'Default page found' + "\t" + 'Xampp',
    b'Test Page for Apache' : 'Default page found  ' + "\t" + 'Outdated Apache Unknown Version',
    # nginx
    b'Welcome to nginx' : 'Default page found' + "\t" + 'Nginx Unknown Version',
    # iis
    b'404 Object Not Found' :  'Default page found  ' + "\t" + 'Outdated IIS5.0',
    b'index.of'  : 'Default page found  ' + "\t" + 'IIS Unknow Version',
    b'Microsoft-IIS/5.0 server at'  : 'Default page found  ' + "\t" + 'Outdated IIS5.0' ,
    b'alt="IIS7"'  : 'Possible Default page found  ' + "\t" + 'Likely IIS7',
    b'Welcome.png'  : 'Possible Default page found  ' + "\t" + 'Likely IIS Unknown Version',
    # advx
    b'Welcome to the Advanced Extranet' : 'Default page found'  + "\t" + 'ADVX ',
    # apache tomcat
    b"If you're seeing this, you've successfully installed Tomcat" : 'Default page found' + "\t" + 'Apache Tomcat',
    # apache axis
    b'Welcome to the new generation of Axis' : 'Default page found' + "\t" + 'Apache Axis application server'
}

# get command line arguments
def setOpts():

    global ifile, reverse
    ifile = False
    reverse = False
    flags = "hrf:"
    longflags = ["help", "reverse", "file"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], flags, longflags)
    except getopt.GetoptError as err:
        usage(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage(0)
            sys.exit
        elif o in ("-f", "--file"):
            ifile = a
            # if file provided is not an actual file
            if not path.isfile(ifile):
                print("\nERROR: invalid file provided to -f or --file argument; for usage info python findDefaultPages.py -h")
                usage(0)
        elif o in ("-r", "--reverse"):
            reverse = True
        else:
            print("\nERROR: unhandled option; for usage info python findDefaultPages.py -h")
            usage(0)

    if not ifile:
        print("\nERROR: no file provided via -f or --file argument; for usage info python findDefaultPages.py -h")
        usage(0)


# print usage message 
def usage(ecode):
    usage = """

    usage: python findDefaultPages.py -h or python findDefaultPages.py -f [file]
    
         -h --help:     display help info
         -r --reverse:  only print URLs or IP addresses where content was found but not default webserver pages
         -f --file:     path to file containing urls or ip addresses to query for default webserver pages

    """
    print(usage)
    sys.exit(ecode)

def search():
    startm = """
    
    ****************** START ****************************
    
    """ 
    print(startm)
    global terms, stats 
    protocols = ['http','https'] 
    url = '' 

    f = open(ifile, "r")
    for l in f:
        l = l.rstrip('\n')
        for p in protocols:
            # build url with protocol and port
            url = p + '://' + str(l)
             
            # make sure connection works
            try: 
                headers = {"User-Agent": "Mozilla/5.0 (windows NT 6.1; Win64; x63)"}
                req = urllib.request.Request(url=url,headers=headers)
                resp = urllib.request.urlopen(req, timeout=3)
            except timeout:
                stats['Timeouts'] += 1
                if not reverse:
                    print('Timeout error against url: ' + str(url))
                continue
            except Exception as e:
                if hasattr(e,'code') and e.code == 404:
                    stats['404s'] += 1
                else:
                    stats['Untracked'] += 1
                if not reverse:
                    print(str(url) + "\t" + str(e))
                continue

            # check contents for particular content
            # use > -1 to check for content to exist
            # use == -1 t check for content not existing
            contents = resp.read()
            found = False
            for t in terms:
                if contents.find(t)>-1:
                    if not reverse:
                        print(url + "\t" + terms[t])
                    stats['Founds'] += 1
                    found = True
                    break 
            if not found:
                print(url + "\t Content found not likely default pages")
                stats['Not Founds'] += 1
    endm = """
    
    ******************* END *****************************

    """

def printStats():
    print('Script encountered ' + str(stats['404s']) + ' 404 error(s)')
    print('Script encountered ' + str(stats['Timeouts']) + ' Connection Timeout(s)')
    print('Script disovered ' + str(stats['Founds']) + ' likely webserver default pages')
    print('Script disovered ' + str(stats['Not Founds']) + ' web pages that are likely not default pages')
    print('Script encountered ' + str(stats['Untracked']) + ' URL(s) or IP(s) which failed to load due to untracked errors.')
    print()
    print('To confirm content not likelyto be default pages, run script with -r flag to reverse the functionality. This will only list results where content was found but default pages were not found. You will need to manually check these results.')
    print()
    
def main():
    setOpts()
    search()
    printStats()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Exiting...");
