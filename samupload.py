#!/usr/bin/env python3
'''
Licensed under MIT License, (c) B. Kerler
'''
import os
import argparse
import sys
import usb.core                 # pyusb
import usb.util
import struct

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

class usb_class():

    def __init__(self):
        VENDOR_SAMSUNG = 0x04e8
        PRODUCT_MODEM = 0x685d
        INTERFACE_EP = 1
        SETTING_EP = 0

        self.device = usb.core.find(idVendor=VENDOR_SAMSUNG, idProduct=PRODUCT_MODEM)
        if self.device is None:
            print("Is the Samsung modem connected ?")
            sys.exit(1)
        self.device.set_configuration()
        self.configuration = self.device.get_active_configuration()
        print(self.configuration)
        for itf_num in [0, 1]:
            itf = usb.util.find_descriptor(self.configuration,
                                           bInterfaceNumber=itf_num)
            try:                               
                if self.device.is_kernel_driver_active(itf_num):
                    print("Detaching kernel driver")
                    self.device.detach_kernel_driver(itf_num)
            except:
                print("No kernel driver supported.")
                
            usb.util.claim_interface(self.device, itf_num)

            self.EP_OUT = usb.util.find_descriptor(itf,
                                                   # match the first OUT endpoint
                                                   custom_match= \
                                                       lambda e: \
                                                           usb.util.endpoint_direction(e.bEndpointAddress) == \
                                                           usb.util.ENDPOINT_OUT)

            self.EP_IN = usb.util.find_descriptor(itf,
                                          # match the first OUT endpoint
                                          custom_match= \
                                              lambda e: \
                                                  usb.util.endpoint_direction(e.bEndpointAddress) == \
                                                  usb.util.ENDPOINT_IN)

    def write(self,command):
        self.device.write(self.EP_OUT,command)

    def read(self,length=0x80000):
        tmp=self.device.read(self.EP_IN, length)
        return bytearray(tmp)


class samsung_upload():

    def __init__(self):
        self.cdc = usb_class()
        self.cdc.write(b"PrEaMbLe\0")
        data = self.cdc.read()
        if (data!=b"AcKnOwLeDgMeNt\x00"):
            print("Sorry, but device isn't in upload mode !")
            exit(0)

    def bytetostr(self,data):
        txt=""
        for i in range(0, len(data)):
            tmp = data[i]
            if (tmp == 0):
                break
            txt += chr(tmp)
        return txt

    def probe(self):
        self.cdc.write(b"PrObE\0")
        data = self.cdc.read()
        count=0
        devicename = self.bytetostr(struct.unpack("16s", data[0:16])[0])
        if (devicename[0]!="+"):
            print("\nProbed device:\n---------------\n32-Bit, Devicename: \"%s\"\n" % devicename)
            probetable=[]
            print("Detected upload areas:\n---------------------")
            for i in range(16,len(data),0x1C):
                [ptype,pname,pstart,pend]=struct.unpack("<I 16s I I",data[i:i+0x1C])
                probetable.append([ptype,self.bytetostr(pname),pstart,pend])
                print("%d:\"%s\" (0x%x,0x%x)" % (count,self.bytetostr(pname),pstart,pend))
                count+=1
        else:
            print("\nProbed device:\n---------------\n64-Bit, Devicename: \"%s\"\n" % devicename[1:])
            probetable = []
            print("Detected upload areas:\n---------------------")
            for i in range(16, len(data), 0x28):
                [ptype, pname, pstart, pend] = struct.unpack("<I 20s Q Q", data[i:i + 0x28])
                probetable.append([ptype, self.bytetostr(pname), pstart, pend])
                print("%d:\"%s\" (0x%x,0x%x)" % (count, self.bytetostr(pname), pstart, pend))
                count += 1

        return probetable

    def command(self,command,ack=True):
        command+=b"\0"
        self.cdc.write(command)
        if ack:
            tmp = self.cdc.read()
            if not b"AcKnOwLeDgMeNt\x00" in tmp:
                return False
        return True

    def download(self,area):
        filename="%s_%x_%x.bin" % (area[1],area[2],area[3])
        filename=os.path.join("memory",filename)
        print_progress(0, 100, prefix='Preparing: \"%s\"' % filename, suffix='', bar_length=50)
        with open(filename,"wb") as wf:
            start=bytes(hex(area[2])[2:],'utf-8')
            end=bytes(hex(area[3])[2:],'utf-8')
            self.command(b"PrEaMbLe")
            self.command(start)
            self.command(end)
            self.command(b"DaTaXfEr",False)
            total=area[3]+1-area[2]
            data=b""
            old=0
            pos=0
            while (pos<total):
                prog = int(float(pos) / float(total) * float(100))
                if (prog > old):
                    print_progress(prog, 100, prefix='Downloading: \"%s\"' % filename, suffix='', bar_length=50)
                    old = prog
                size=total-pos
                if (size>0x80000):
                    size=0x80000
                data=self.cdc.read(size)
                self.command(b"AcKnOwLeDgMeNt",False)
                wf.write(data)
                pos+=len(data)
            print_progress(100, 100, prefix='Done: \"%s\"' % filename, suffix='', bar_length=50)

def main():
    parser = argparse.ArgumentParser(description='SUC - Samsung Upload Client (c) B.Kerler 2018.')

    print("\nSUC - Samsung Upload Client v1.0 (c) B. Kerler 2018, Email: info @ revskills.de")
    parser.add_argument(
        '--area', '-a',
        help='Select area to dump',
        default='')
    parser.add_argument(
        '--all', '-all',
        help='Download all areas',
        action="store_true")
    args = parser.parse_args()

    suc=samsung_upload()
    areas=suc.probe()
    if (os.path.exists("memory")):
        shutil.rmtree("memory")
    os.mkdir("memory")

    if args.area!="":
        print("\nDownloading ....\n-----------------")
        area=int(args.area)
        if len(areas)<=area:
            print("Sorry, but area number is too high")
            exit(0)
        suc.download(areas[area])
        suc.command(b"PoStAmBlE")
    elif args.all==True:
        print("\nDownloading ....\n-----------------")
        for area in areas:
            suc.download(area)
        suc.command(b"PoStAmBlE")
    else:
        print("\nRun 'samupload.py -all' to dump all areas")
        print("Run 'samupload.py -a [number]' to dump specific area")


    print("Done. Dumped memory has been written to memory directory.")

if __name__ == '__main__':
    main()
