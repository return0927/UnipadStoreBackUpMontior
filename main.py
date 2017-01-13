import requests, os, threading
from time import sleep, strftime
os.chdir("/logs/")



def getjson():
    return __import__("json").loads(requests.get("http://rdp.unipad.kr/store/getList.php").text)

def save_data():
    html = getjson()
    day = strftime("%Y %m %d %H")
    t = strftime("%Y-%m-%d %H.%M.%S")
    if not os.path.isdir(day):
        os.mkdir(day)
    os.chdir(day)
    with open(t+".txt", "w") as out:
        out.write(str(html))
    os.chdir("../")
    print(t + " | " + str(len(str(html))))
    sleep(60)
    

def getdata():
    data = getjson()
    totalc = data['totalCount']
    packs = list()

    for pack in data['list']:
        packs.append(pack)

    """
    code
    isAutoPlay
    title
    isLED
    producerName
    downloadCount
    """
    
    ret = list()
    ret.append("\n   totalCount : %s\n\n" % "{:,}".format(totalc))
    for d in packs:
        ret.append("   %-40s | %15s | %s" % (d['title'], "{:,}".format(int(d['downloadCount'])), d['producerName']))
    
    return ret

def updatevalue():
	text = ""
	for l in getdata():
		text = text + l + "\n"
	lb.config(text=text, justify="left", font = ('굴림체', 10))

from tkinter import *

def monitor():
    
    root=Tk()
    lb = Label(root);
    lb.pack(anchor = "w")
    data = getdata()

    while(1):
        text = ""
        for l in getdata():
            text = text + l + "\n"
        lb.config(text=text, justify="left", font = ('굴림체', 10))
	
        root.update() 
    #    __import__("time").sleep(2)



backup = threading.Thread(target=save_data)
backup.start()

mon = threading.Thread(target=monitor)
mon.start()
