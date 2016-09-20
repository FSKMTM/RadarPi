import serial, time, signal, sys, os, pynmea2, threading


s = serial.Serial()
s.baudrate = 115200
s.timeout = 0
s.port = "/dev/ttyAMA0"

s_led = serial.Serial()
s_led.baudrate = 9600
s_led.timeout = 0
s_led.port = "/dev/ttyUSB0"

s_gps=serial.Serial()
s_gps.baudrate = 9600
s_gps.timeout = 0
s_gps.port = "/dev/ttyACM0"

#Definicija spremenljivk
speed=0 #Mora biti nekaj majhnega za zacetek
VR_dej=999 #Mora biti nekaj zelo velikega za zacetek
start_time=time.time()



timelabel = time.strftime("%Y_%d_%m-%H_%M_%S")

f = open("radar_data"+timelabel+".txt", "w")

try:
    s_led.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)

try:
    s_gps.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)

def sigint_handler(signum, frame):
    print ("User interrupted, exiting \r")
    s_led.write("$$$ALL,OFF\r")
    sys.exit()
signal.signal(signal.SIGINT, sigint_handler)

#Funkcija vnasanje komand
def vnasanje_komand():
    command_list=['s','b','t','v']
    command_list2=['1','2']
    prikaz_targets=3
    prva_komanda=raw_input("Vnesi prvo komando [na voljo: s,b,t,v]: ")
    if prva_komanda not in command_list:  #preverim, ce je vnesena komanda sploh med tistimi, ki so na voljo
        print("Vnesena je napacna komanda! Poizkusite ponovno.") #vrne v vnasanje komand
        return 0

    if prva_komanda=="t":
        prikaz_targets=raw_input("Za izpis samo targetov pritisni 1, za poln izpis pritisni 2: ")
        while prikaz_targets not in command_list2:
            prikaz_targets=raw_input("Vnesete lahko le 1 ali 2, prosimo vnesite ukaz ponovno:")
            
    druga_komanda=raw_input("Vnesi drugo komando: ")

    time.sleep(0.25)
    s.write(prva_komanda)
    time.sleep(0.25)
    s.write(druga_komanda)
    time.sleep(0.25)
    s.write("s")
    time.sleep(0.25)
    return prikaz_targets

#Funkcija pisanja informacij GPS-a
def GPS_info(previous_vtg):
    a_gps=s_gps.readline()
    b_gps=a_gps.split(',')

##    while b_gps[0]!="$GPGGA": #Pocakam, da parsam pravo informacijo oz. pravo vrstico (to je pripravljeno, ce bom rabil koordinate in cas)
##        a_gps=s_gps.readline()
##        b_gps=a_gps.split(',')
##        
##    msg=pynmea2.parse(a_gps)
##    time_gps=msg.timestamp
##    coord_lat=msg.lat,msg.lat_dir
##    coord_lon=msg.lon,msg.lon_dir
        
    if b_gps[0]=="$GPVTG": #Pocakam, da parsam pravo informacijo oz. pravo vrstico
        msg=pynmea2.parse(a_gps)
        vtg=msg.spd_over_grnd_kmph
        if vtg==None: #V primeru da ni GPS signala in je vtg=None, npr. v tunelu
            vtg=0
    else:
        vtg=previous_vtg #zato, da ostane zapisana zadnja znana vrednost  
    return vtg

#Izracun varnostne razdalje glede na informacije GPS-a
def VR_teor_calc(speed):
    VR_t=(speed/3.6)*2
    return VR_t

#Pisanje informacij radarja
def WRITE_radar(prikaz,previous_VR_d):
    VR_d=999 #Mora biti nekaj zelo velikega za zacetek
    a=s.readline()
    b=a.split(' ')

    if a=='': #izlocim prazne vrste, ki verjetno nastanejo zaradi tega, ker je Raspi prehiter glede na 100 ms sample rate od radarja
        VR_d=previous_VR_d
        return VR_d


    elif b[0]=="T0": 
        Range_T0=int(b[1]) #Pretvorim razdalje iz string v integer, da lahko kasneje z njimi operiram
        Range_T1=int(b[5])
        Range_T2=int(b[9])
        Range_T3=int(b[13])
        Range_T4=int(b[17])
        
        i=1
        R=[]
        while i<=17:  #filter za 0, ki pomeni, da targeta sploh ni
            if int(b[i])!=0:
                R.append(int(b[i]))
            i=i+4
            
        if R: #Preverim, da R ni prazen array, kar pomeni da so same nule - vrednost mora biti TRUE        
            VR_d=min(R)
        else:
            VR_d=999

        
        if VR_d==23 or VR_d==71 or VR_d<3: #Naredim filter za bina 23 in 71, ki jih jemljemo kot motnjo 
            VR_d=previous_VR_d
            return VR_d

        if prikaz=="1": #preverim,da je izbran samo izpis targetov
            print Range_T0,Range_T1,Range_T2,Range_T3,Range_T4
            f.write('%4.02f' % (time.time()-initial_time)+"\t"+'%d' % Range_T0+"\t"+'%d' % Range_T1+"\t"+'%d' % Range_T2+"\t"+'%d' % Range_T3+"\t"+'%d' % Range_T4+"\t"+'%g' % speed+"\r\n")#zapisovanje podatkov v file
            f.flush()
        elif prikaz=="2": #preverim, da je izbran poln izpis
            print a
            f.write('%4.02f' % (time.time()-initial_time)+"\t"+a.rstrip('\n')+"\t"+'%g' % speed+"\r\n")#zapisovanje podatkov v file
            f.flush()

    elif b[0][0]=="B": #preverim, da je prva informacija v stringu crka B
        print a
        f.write(a)#zapisovanje podatkov v file
        f.flush()

    return VR_d

#Funkcija prikaza opozorila na LED matricnem zaslonu
def prikaz_opozorila():
    if VR_dej==999:
        s_led.write("$$$T5,1,-\r")
    else:   
        range_parse=list(str(VR_dej))        
        i=len(range_parse)
        n=0
        s=3 #lokacija prvega stevila na zaslonu
        while n<=(i-1): #glede na to ali imamo eno ali dvomestno stevilo
            s_led.write("$$$T"+str(s)+",2,"+range_parse[n]+"\r")
            n=n+1
            s=s+5


prikaz_targets=vnasanje_komand()   
while prikaz_targets==False:
    prikaz_targets=vnasanje_komand()

#V file naprintam glavo: SW version in imena stolpcev
while 1:
    A=s.readline()
    B=A.split(' ')
    if B[0]=="SW":
        break
print(A)
f.write(A+"\r\n")
if prikaz_targets=="1":
    f.write("Time"+"\t"+"T1"+"\t"+"T2"+"\t"+"T3"+"\t"+"T4"+"\t"+"T5"+"\t"+"V_GPS"+"\r\n")

global initial_time
initial_time=time.time()

#glavna neskoncna zanka  
while 1:
    VR_dej=WRITE_radar(prikaz_targets,VR_dej)
    speed=GPS_info(speed)
    VR_teor=VR_teor_calc(speed)


#Primerjava varnostne razdalje in izvrsitev ukaza
    if  (time.time()-start_time)>0.5: #Nov thread naredim sele ko se prvi do konca izvede (cca. 6,5 sekund za izpis na zaslon) in kadar je hitrost vecja od 20 km/h
        t1=threading.Thread(target=prikaz_opozorila) #Naredim threading, ker ce bi bilo prikazovanje opozorila v isti while zanki, bi informacijo radarja prejel le ko se izvrsi funkcija prikaz opozorila
        t1.start()
        start_time=time.time()
        s_led.write("$$$ALL,OFF\r")

        
        

        
    



