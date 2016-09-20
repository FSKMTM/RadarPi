from threading import Thread

def printaj():
    print "hello"

def printaj_2():
    print "world!"
    a=10
    return a


    
t1 = Thread(target = printaj)
t2 = Thread(target = printaj_2)

t1.start()
t2.start()

print a

