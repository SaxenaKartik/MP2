from threading import Thread
import http.client, sys
from queue import Queue
import hashlib, time
from  urllib.parse import urlparse
concurrent = 1
import requests

def hashit(k : str):
    hash = hashlib.sha1()
    hash.update(k.encode('utf-8'))
    return  hash.hexdigest()[:-10]


def doWork():
    while True:
        url = q.get()
        status, url = getStatus(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        # url = urlparse(ourl)
        # print(url.path)
        # conn = http.client.HTTPConnection(url.netloc, "8080")
        # conn.connect()
        # conn.request("GET",url.path, "")
        # res = conn.getresponse()
        # conn.close()
        # print(res.read())
        res = requests.get(ourl)
        print(res.text)
        return(res.status_code, ourl)
    except:
        return("error", ourl)

def doSomethingWithResult(status, url):
    print(status, url)


drone_id = "00000000e215b4a2"
hash_drone_id = "7110eda4d09e062aa5e4a390b0a572"
# print(hash_drone_id)
q = Queue(concurrent)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    # url = "https://192.168.1.101/api/drone/"
    for i in range(1):
        q.put("http://192.168.1.101:8080/api/drone/7110eda4d09e062aa5e4a390b0a572")
    q.join()
except KeyboardInterrupt:
    sys.exit(1)
