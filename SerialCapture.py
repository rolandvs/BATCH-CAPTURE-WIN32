#!c:\python27\python.exe

# based on tcp_serial_redirect.py from pyserial
# http://pyserial.sourceforge.net/



import  sys, os, threading, getopt, socket, datetime


try:
    import serial 
except:
    print ("Unexpected serial import error Line 14")
    raw_input('Press Enter To Exit')
    sys.exit(1)

try:
    True
except NameError:
    True
    False


class SerialCapture(object):
    def __init__(self,com_port, baudrate=9600, rtscts=False,
                 xonxoff=False, timeout=90):
        
    # create the serial connection
        ser = serial.Serial()
        ser.port    = com_port
        ser.baudrate = baudrate
        ser.rtscts  = rtscts
        ser.xonxoff = xonxoff
        ser.timeout = timeout     #required so that the reader thread can exit
        try:
            ser.open()
        except serial.SerialException as e:
            print ("Could not open serial port %s: %s" % (ser.portstr, e))
            raw_input('Press Enter To Exit')
            sys.exit(1)
        self.serial = ser

    def go(self):
        self.alive = True
        self.reader()
    
        
    def reader(self):
        print ("Serial Capture Started Using Port %s %s\n\n" % (self.serial.portstr, str(datetime.datetime.now())))
        data = None
        data_on = 2
        while not data:
            data = self.serial.read(1)              #read one, blocking
            n = self.serial.inWaiting()             #look if there is more
            sys.stdout.flush()
        while self.alive:
            try:
                if n:
                    data = data + self.serial.read(n)  #and get as much as possible
                if data:
                    logfile = open("active_log.txt","a")
                    logfile.write(str(data .decode('latin1')))
                    #print str(data .decode('latin1')), #For Testing
                    logfile.close()
                    if not data_on == 1:
                        print("DATA RECEIVED  " + str(datetime.datetime.now()))
                        statusfile = open("status_log.txt","a")
                        statusfile.write("DATA RECEIVED  %s\n\n" % str(datetime.datetime.now()))
                        statusfile.close()
                    data_on = 1
                    sys.stdout.flush()
                else:
                   if data_on == 1:
                        print ("SERIAL PORT IDLE  %s\n\n" % str(datetime.datetime.now()))
                        statusfile = open("status_log.txt","a")
                        statusfile.write("SERIAL PORT IDLE  %s\n\n\n\n" % str(datetime.datetime.now()))
                        statusfile.close()
                        data_on = 0
                data = self.serial.read(1)              #read one, blocking
                n = self.serial.inWaiting()             #look if there is more
                sys.stdout.flush()
            except socket.error as msg:
                print (msg)#probably got disconnected
                raw_input('Press Enter To Exit')
                break
        self.alive = False
        self.serial.close()
        if self.thread_write:
            self.thread_write.join()
    

    def stop(self):
        """Stop copying"""
        if self.alive:
            self.alive = False
            self.thread_write.join()

if __name__ == '__main__':
    
    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                "hp:b:rxP:",
                ["help", "port=", "baud=", "rtscts", "xonxoff", "ipport="])
    except getopt.GetoptError:
        # print help information and exit:
        print >>sys.stderr, __doc__
        raw_input('Press Enter To Exit')
        sys.exit(2)
    
    ser_port = str(raw_input('Enter port name: \nExample: COM1\n'))
    baudrate = 9600
    rtscts = False
    xonxoff = False
    for o, a in opts:
        if o in ("-h", "--help"):   #help text
            usage()
            raw_input('Press Enter To Exit')
            sys.exit()
        elif o in ("-p", "--port"):   #specified port
            try:
                ser_port = int(a)
            except ValueError:
                ser_port = a
        elif o in ("-b", "--baud"):   #specified baudrate
            try:
                baudrate = int(a)
            except ValueError:
                raise ValueError ("Baudrate must be a integer number")
        elif o in ("-r", "--rtscts"):
            rtscts = True
        elif o in ("-x", "--xonxoff"):
            xonxoff = True


    print ("\n---Serial Capture ---\nVersion Win32_1 2-Dec-2013 By -DL-\n\n")


    while 1:
        try:
            #enter console->serial loop
            r = SerialCapture(ser_port, baudrate,
                              rtscts, xonxoff)
            r.go()
        except socket.error as msg:
            print (msg)

    print ("\n--- exit ---")


