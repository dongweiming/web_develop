# coding=utf-8
import time


def func1():
    sum = 0
    for i in range(100000):
        sum += i


def func2():
    time.sleep(10)


func1()
func2()
