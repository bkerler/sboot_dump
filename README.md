# SUC - Samsung Upload Client v1.0 
## (c) B. Kerler 2018-2022, licensed under MIT License

A tool to dump RAM using S-Boot Upload Mode (in python)

Thx to Nitay Artenstein's code at https://github.com/nitayart/sboot_dump, ported
to python and added full support based on reversing sboot

### Supported
- Samsung QC
- Samsung MTK
- Samsung Unisoc not yet supported

### Install
- Python 3.6 or higher
``
pip install pyusb pyserial
``

### Show partition table on the device
``
python3 scripts/samsungupload.py
``

#### For dumping all memory areas:

``
python3 scripts/samsungupload.py all
``

#### For dumping a specfic memory range:

``
python3 scripts/samsungupload.py range 0x0 0xffffffff
``

#### For dumping a full memory range:

``
python3 scripts/samsungupload.py full
``

#### For dumping individual areas (Index 0):

``
python3 scripts/samsungupload.py partition 0
``

### Windows install
- Install usbdk and make sure to remove old libusb dlls from windows/system32 folder.
  Get the usbdk installer (.msi) from [here](https://github.com/daynix/UsbDk/releases/) and install it
- Install normal Samsung Serial Port driver (or use default Windows COM Port one, make sure no exclamation is seen)

### Linux install

```bash
sudo apt purge ModemManager
sudo usermod -aG plugdev $USER
sudo usermod -aG dialout $USER
sudo cp Drivers/*.rules /etc/udev/rules.d
sudo udevadm control -R
```

- Log in and out user

```bash
sudo pip3 install -r requirements
```

Enjoy !
