import sys, os
sys.path.append("..")

from servos.ardSerial import keepCheckingPort, connectPort, send, closeAllSerial
import threading

#'kbalance','kbuttUp','kcalib','kdropped','klifted','klnd','krest','ksit','kstr','kup','kzero','kang','kbx','kchr','kck','kcmh','kdg','kfiv','kgdb','khds','khg','khi','khsk','khu','kjmp','kkc','kmw','knd','kpd','kpee','kpu','kpu1','krc','kscrh','ksnf','ktbl','kts','kwh','kzz', "kwkF", "kwkB", "kwkL", "kwkR"

def main():
    goodPorts = {}
    connectPort(goodPorts)
    t = threading.Thread(target=keepCheckingPort, args=(goodPorts,))
    t.start()
    
    send(goodPorts, ['g',0.1])
    send(goodPorts, ['z',0.1])
    
    while True:
        s = input(">")
        if (s == 'q'):
            break
        send(goodPorts, ["k"+s, 0])

    closeAllSerial(goodPorts)
    os._exit(0)

if __name__ == "__main__":
    main()