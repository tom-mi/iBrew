;iBrew Installer
!addplugindir .

!include release.nsh

;--------------------------------
;Include Modern UI

!include "MUI2.nsh"

;--------------------------------

;General
	;file name
	;OutFile "iBrew ${RELEASE_STR}.exe"
	OutFile "iBrew.exe"

	;Default installation folder
	InstallDir "$PROGRAMFILES\iBrew"

	;Request application privileges for Windows Vista
	RequestExecutionLevel admin

	InstallDirRegKey HKLM "Software\iBrew" ""

	;Show all languages, despite user's codepage
	;!define MUI_LANGDLL_ALLLANGUAGES

;--------------------------------
;Variables

  Var StartMenuFolder 
	
;--------------------------------
;Interface Configuration

	!define MUI_ICON "..\..\resources\favicon.ico"
	!define MUI_WELCOMEFINISHPAGE_BITMAP "side.bmp"  ;shoukd be 164x314
	!define MUI_HEADERIMAGE
	!define MUI_HEADERIMAGE_BITMAP "top.bmp" ; ;should be 150x57
	;!define MUI_ABORTWARNING
	!define MUI_WELCOMEPAGE_TITLE $(app_WelcomePageTitle)
	!define MUI_WELCOMEPAGE_TEXT $(app_WelcomePageText) 

	!define  MUI_LICENSEPAGE_TEXT_TOP $(app_LicensePageTextTop)
	;!define  MUI_LICENSEPAGE_TEXT_BOTTOM  $(app_LicensePageTextBottom)
	;!define  MUI_LICENSEPAGE_CHECKBOX	
	
	;!define MUI_FINISHPAGE_NOAUTOCLOSE

	;!define MUI_FINISHPAGE_SHOWREADME "release_notes.txt"
	;!define MUI_FINISHPAGE_SHOWREADME_TEXT "Show Release Notes"
	;!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
	
	!define MUI_FINISHPAGE_TITLE $(app_FinishPageTitle)
	!define MUI_FINISHPAGE_TEXT $(app_FinishPageText)

	!define MUI_FINISHPAGE_LINK $(app_FinishPageLink)
	!define MUI_FINISHPAGE_LINK_LOCATION  "https://github.com/Tristan79/iBrew/"

	;Start Menu Folder Page Configuration
	!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKLM" 
	!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\iBrew"
	!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
	!define MUI_STARTMENUPAGE_DEFAULTFOLDER "iBrew"
    
	;--------------------------------
;Pages

	!insertmacro MUI_PAGE_WELCOME
	
    !insertmacro MUI_PAGE_LICENSE "LICENSE"

	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
	!insertmacro MUI_PAGE_INSTFILES
	!insertmacro MUI_PAGE_FINISH
 
;--------------------------------
;Languages
!include "languages.nsh"

;--------------------------------
;Reserve Files
  
  ;If you are using solid compression, files that are required before
  ;the actual installation should be stored first in the data block,
  ;because this will make your installer start faster.
  
  !insertmacro MUI_RESERVEFILE_LANGDLL

;--------------------------------
	;App Name and file
	Name "$(app_AppName) ${RELEASE_STR}"

;Installer Sections

Section "Install Section" SecInstall

	SetOutPath "$INSTDIR"
	File /r ..\..\dist\ibrew\*
	;File ..\..\release_notes.txt

	;Store installation folder
	WriteRegStr HKLM "Software\iBrew" "" $INSTDIR

	;  Add registry entries for Control Panel Uninstall
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew" \
                 "DisplayName" "iBrew"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew" \
                 "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew" \
                 "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"	
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew" \
                 "DisplayVersion" "${RELEASE_STR}"	
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew" \
                 "Publisher" "iBrew"
				 
	;Create uninstaller
	WriteUninstaller "$INSTDIR\Uninstall.exe"

	!insertmacro MUI_STARTMENU_WRITE_BEGIN Application

		;Create shortcuts
		CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
		CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
		CreateShortCut "$SMPROGRAMS\$StartMenuFolder\iBrew.lnk" "$INSTDIR\ibrewui.exe"

	!insertmacro MUI_STARTMENU_WRITE_END

	CreateShortCut "$DESKTOP\iBrew.lnk" "$INSTDIR\ibrewui.exe" ""

	
SectionEnd

;--------------------------------
;Installer Functions

Function .onInit

  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd


;--------------------------------
;Uninstaller Section

Section "Uninstall"

	Delete "$INSTDIR\*"

	Delete "$INSTDIR\Uninstall.exe"

	RMDir /r "$INSTDIR"

    Delete "$DESKTOP\iBrew.lnk"

	!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

		Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
		Delete "$SMPROGRAMS\$StartMenuFolder\iBrew.lnk"
		RMDir "$SMPROGRAMS\$StartMenuFolder"

	DeleteRegKey /ifempty HKLM "Software\iBrew"
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\iBrew"
	
SectionEnd


