# SUC - Samsung Upload Client v1.0 
## (c) B. Kerler 2018, licensed under MIT License

A tool to dump RAM using S-Boot Upload Mode (in python)

Thx to Nitay Artenstein's code at https://github.com/nitayart/sboot_dump, ported
to python and added full support based on reversing sboot
  
Run
---
``
python3 scripts/samsungupload.py
``

- For dumping all memory areas:

``
python3 scripts/samsungupload.py -all
``

- For dumping individual areas (Index 0):

``
python3 scripts/samsungupload.py -a 0
``

Issues
------
- For windows usage, install libusb kernel filter driver:
  https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/libusb-win32-devel-filter-1.2.6.0.exe/download

Enjoy !
