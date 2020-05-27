from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
import os
import time
import json
import sys
import subprocess
import datetime
from socket import timeout

def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    global info
    global quality
    quality = "best"
    url = 'http://goodgame.ru/api/getchannelstatus?id=' + user + '&fmt=json'
    status = 3 ###
    try:
        info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
        for key in info.keys():
            if info[key]['status'] == "Dead":
                status = 1
            else:
                status = 0
            
    except (HTTPError, URLError) as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    except timeout:
        print("Connection timed out! Waiting for 30 seconds...")
        status = 3
    except BaseException as error:
        print('An exception occurred: {}'.format(error))
    except:
        print('WTF Happened?!')
    return status
 
def format_filename(fname):
# Removes invalid characters from filename
    fname = fname.replace("/","")
    fname = fname.replace("?","")
    fname = fname.replace(":","-")
    fname = fname.replace("\\","")
    fname = fname.replace("<","")
    fname = fname.replace(">","")
    fname = fname.replace("*","")
    fname = fname.replace("\"","")
    fname = fname.replace("|","")
    return fname

def rec_check(isOn):
	# nevermind
    my_file = open("C:\\test\\"+user+".txt", 'w')
    if isOn == True:
        my_file.write('1')
    else:
        my_file.write('0')
    my_file.close()
 
def loopcheck():
    while True:
        status = check_user(user)
        if status == 2:
            print("username not found. invalid username?")
            rec_check(False)
        elif status == 3:
            print(datetime.datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 30 seconds.")
            rec_check(False)
            time.sleep(30)
        elif status == 1:
            print(datetime.datetime.now().strftime("%Hh%Mm%Ss"),user,"currently offline, checking again in",refresh,"seconds")
            rec_check(False)
            time.sleep(refresh) # 30 seconds
        elif status == 0:
            print(user,"online. stop.")
            rec_check(True)
            filename = user+" - "+datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss")+".mp4"
            filename = format_filename(filename)
            #process = subprocess.Popen(['python', 'gege_chat_gg.py'], stdout = subprocess.PIPE )
            subprocess.call(["streamlink", "goodgame.ru/channel/"+user,quality,"-o", directory+filename])
            #process.kill()
            print("Stream is done. Going back to checking..")
            rec_check(False)
            time.sleep(15)
 
def main():
    global refresh
    global user
    global directory
 
    refresh = 30.0
    directory = "C:\\VODs\\"
 
    client = False
    clientID = "http-header=Client-ID=CLIENT_ID"
    dir_path = '%s\streamlink\streamlinkrc' % os.environ['APPDATA']
 
    file = open(dir_path, 'r')
    for line in file:
        if line == clientID:
            client = True
    file = open(dir_path, 'a')
    if client != True:
        file.write(clientID)
    file.close()
 
    if(refresh<15):
        print("Check interval should not be lower than 15 seconds")
        refresh = 15
 
    #print("Checking for",user,"every",refresh,"seconds. Record with",quality,"quality.")
    loopcheck()
 
 
if __name__ == "__main__":
    # execute only if run as a script
    user = str(sys.argv[1])
    main()
