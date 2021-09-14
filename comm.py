from socket import socket

from random import random
import math


ms = socket()
ms.bind(('localhost',5000))
ms.listen(5)
c = []
x = []
def mean(arr):
    k = 0
    for i in arr:
        k = k + i/len(arr)
    return(k)
        
def generat_random_position():
    c.append(round(random()*400))
    x.append(round(random()*400))
    return(mean(c),mean(x)) 
def gen_rPath():
    pass
g = 0
while True:
    conexion, addr = ms.accept()
    if(len(c)>400):
        c = []
        x = []
    a,b = generat_random_position()
    
    msn = str(int(a))+','+str(int(b))
    a = "{0:b}".format(int(a))
    a = bytes(a, 'utf-8')
    print(a)
    if(g == 0):
        conexion.send("nHLvci77SZkVgIVldp6cVWLh8AnSglLFgdR6W2KXqISBfOXTn2C9KV3Rp7awQtfZJE6nzUpcc0faAh5mSoFHIBjZD8g448ppOvZyNzRxOyzYIvwakL26d5jYfCw2ZpBfMTJphDlhzS3I1ALqUOXdw2ghxotssG6OPAoOIG6mPkTDfZiMaf48qAh3iD16pVlcH9Tz3S9jzsGVzyQPbtJS8YTTWJMJFFEEqw3BqHo48S0j0PAgFilyPrdVoPNZ80rP\nnHLvci77SZkVgIVldp6cVWLh8AnSglLFgdR6W2KXqISBfOXTn2C9KV3Rp7awQtfZJE6nzUpcc0faAh5mSoFHIBjZD8g448ppOvZyNzRxOyzYIvwakL26d5jYfCw2ZpBfMTJphDlhzS3I1ALqUOXdw2ghxotssG6OPAoOIG6mPkTDfZiMaf48qAh3iD16pVlcH9Tz3S9jzsGVzyQPbtJS8YTTWJMJFFEEqw3BqHo48S0j0PAgFilyPrdVoPNZ80rP".encode())
        g == 1
    if(g == 1):
        conexion.send(str(int(b)).encode())
        g == 0
    
    print("les gooo")
    print(addr)
    print(msn)

    conexion.close()