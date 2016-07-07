# coding=utf-8
import threading
mydata = threading.local()
mydata.number = 42
print mydata.number
log = []


def f():
    mydata.number = 11
    log.append(mydata.number)


thread = threading.Thread(target=f)
thread.start()
thread.join()
print log
print mydata.number
