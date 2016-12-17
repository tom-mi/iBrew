all:
	@echo "iBrew setup (windows, linux & mac)"
	@echo use \"make setup\" to fetch requirements
	@echo use \"make cleanlin\" to clean temp files
	@echo use \"make cleanmac\" to clean temp files
	@echo use \"make cleanwin\" to clean temp files
	@echo use \"make setupmac\" to fetch additional mac requirements for release
	@echo use \"make setupwin\" to fetch additional windows requirements for release
	@echo use \"make mac\" to make a mac release
	@echo use \"make win\" to make a windows release
	@echo use \"make readme\" to create a new README.md 
	@echo use \"make pyinstaller\" to download already patched osx pyinstaller

mac:	cleanlin buildmac cleanmac diskimage

win:	cleanwin buildwin installer

installer:
	@echo !define RELEASE_STR v0.5.0.1 > distro\win\release.nsh
	@copy LICENSE distro\win
	@"C:\Program Files (x86)\NSIS\makensis.exe" distro\win\ibrew.nsi
	@mkdir release
	@move distro\win\iBrew.exe release

buildwin:
	@echo iBrew: Building Windows package    
	@pyinstaller -c --version-file distro\win\version.py -i resources\favicon.ico ibrewlegacy
	@pyinstaller -c --version-file distro\win\version.py -i resources\favicon.ico ibrew
	@pyinstaller -w --version-file distro\win\version.py -i resources\favicon.ico ibrewui
	@mkdir dist\ibrew\resources
	@mkdir dist\ibrew\web
	@xcopy /S resources dist\ibrew\resources
	@xcopy /S web dist\ibrew\web
	@copy /Y dist\ibrewlegacy\*.* dist\ibrew
	@copy /Y dist\ibrewui\*.* dist\ibrew
	@copy LICENSE dist\ibrew

readme:
	@python ibrew license > LICENSE
	@echo iBrew: Generating README.md
	@python ibrew usage > usage.tmp
	@python ibrew examples > examples.tmp
	@python ibrew commands > console.tmp
	@python ibrew notes > notes.tmp
	@python ibrew structure > protocol.tmp
	@cat distro/README.md_parts/README_part1.md usage.tmp distro/README.md_parts/README_part2.md console.tmp distro/README.md_parts/README_part3.md examples.tmp distro/README.md_parts/README_part4.md LICENSE > README.md

setup:
	@echo iBrew: Fetching python requirements
	@pip install -q -r requirements.txt

cleanlin:
	@echo iBrew: Cleaning up
	@rm -f *.pyc smarter/*.pyc
	@rm -f *.tmp
	@rm -rf dist
	@rm -f *.spec 
	@rm -rf build
	@rm -rf test

setuplin: setup bonjourwin

setupwin: setup packwin pyinstaller bonjourwin 

packwin:
	@pip install win-inet-pton

setupmac: setup packmac bonjour pyinstaller

packmac:
	@pip install -q -r distro/mac/requirements.txt

bonjour:
	@curl https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pybonjour/pybonjour-1.1.1.zip > pybonjour-1.1.1.zip
	@pip install pybonjour-1.1.1.zip
	@rm pybonjour-1.1.1.zip

bonjourwin:
	@powershell -command "& { iwr https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pybonjour/pybonjour-1.1.1.zip -OutFile pybonjour-1.1.1.zip }"
	@pip install pybonjour-1.1.1.zip
	@del pybonjour-1.1.1.zip

pyinstaller:
	@git clone https://github.com/Tristan79/pyinstaller.git

cleanwin:
	@echo iBrew: Cleaning up [Windows]
	@distro\win\cleanwin.bat     
 
cleanmac:
	@echo iBrew: Cleaning up [MacOS]
	@rm -rf ~/Library/Application\ Support/iBrew/logs 
	@rm -f *.pyc smarter/*.pyc
	@rm -f *.tmp
	@rm -f *.spec 
	@rm -rf build
	@rm -rf dist/iBrew
	@rm -rf dist/iBrewConsole
	
buildmac:
	@echo iBrew: Building MacOS package
	@rm -rf build     
	@echo Please install upx with: brew install upx
	@pyinstaller ibrewui -s -w -n iBrew --noupx
	@pyinstaller ibrew -s -w -n iBrewConsole --noupx
	@pyinstaller ibrewlegacy -s -w -n iBrewLegacyConsole --noupx
	@cp -a resources dist/iBrew.app/Contents/MacOS
	@cp -a web dist/iBrew.app/Contents/MacOS
	@cp distro/mac/Info.plist dist/iBrew.app/Contents/
	@mv dist/iBrewConsole.app/Contents/MacOS/iBrewConsole dist/iBrew.app/Contents/MacOS
	@mv dist/iBrewLegacyConsole.app/Contents/MacOS/iBrewLegacyConsole dist/iBrew.app/Contents/MacOS
	@cp distro/mac/iBrew.icns dist/iBrew.app/Contents/Resources/icon-windowed.icns
	@rm -rf dist/iBrewConsole.app
	@rm -rf dist/iBrewConsoleLegacy.app
	@mkdir -p test
	@mv dist/iBrew.app test
	@rm -rf dist

diskimage:
	#Set up disk image staging folder
	@rm -rf dmg/iBrew
	mkdir -p dmg/iBrew
	cp LICENSE dmg/iBrew
	ln -s /Applications dmg/iBrew/Applications
	cp -a test/iBrew.app dmg/iBrew
	cp distro/mac/iBrew.icns dmg/iBrew/.VolumeIcon.icns
	SetFile -c icnC dmg/iBrew/.VolumeIcon.icns
	
	##generate raw disk image
	rm -f iBrew.dmg
	hdiutil create -srcfolder dmg/iBrew -volname iBrew-0.5.0 -format UDRW -ov raw-iBrew.dmg	

	#remove working files and folders
	rm -rf dmg/iBrew
	
	# we now have a raw DMG file.
	
	# remount it so we can set the volume icon properly
	mkdir -p dmg/iBrew
	hdiutil attach raw-iBrew.dmg -mountpoint dmg/iBrew
	SetFile -a C dmg/iBrew
	
	hdiutil detach dmg/iBrew
	rm -rf dmg
	
	# convert the raw image
	rm -f iBrew.dmg
	hdiutil convert raw-iBrew.dmg -format UDZO -o iBrew.dmg
	rm -f raw-iBrew.dmg
	
	#move finished product to release folder
	mkdir -p release
	mv iBrew.dmg release
	
