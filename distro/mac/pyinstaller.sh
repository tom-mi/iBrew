#!/bin/bash
git clone https://github.com/Tristan79/pyinstaller.git
cd pyinstaller/bootloader/
python ./waf distclean all
cd ..
python setup.py install
cd ..	
rm -rf pyinstaller
