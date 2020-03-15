#coding:utf-8
from threading import Thread
from time import sleep

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def A(a):
    sleep(5)
    print(a)

