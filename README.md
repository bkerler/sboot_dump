# SUC - Samsung Upload Client v1.0 
## (c) B. Kerler 2018-2022, licensed under MIT License

A tool to dump RAM using S-Boot Upload Mode (in python)

Thx to Nitay Artenstein's code at https://github.com/nitayart/sboot_dump, ported
to python and added full support based on reversing sboot

### Install
- Python 3.6 or higher
``
pip install pyusb pyserial
``

### Run
``
python3 scripts/samsungupload.py
``

#### For dumping all memory areas:

``
python3 scripts/samsungupload.py -all
``

#### For dumping individual areas (Index 0):

``
python3 scripts/samsungupload.py -a 0
``

### Windows usage
- Install usbdk and make sure to remove old libusb dlls from windows/system32 folder.
  Get the usbdk installer (.msi) from [here](https://github.com/daynix/UsbDk/releases/) and install it
- Install normal Samsung Serial Port driver (or use default Windows COM Port one, make sure no exclamation is seen)


Enjoy !
