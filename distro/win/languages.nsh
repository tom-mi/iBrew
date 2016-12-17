;--------------------------------------------------------------------------------------
;------------ ENGLISH -----------------------------------------------------------------
;--------------------------------------------------------------------------------------
!insertmacro MUI_LANGUAGE "English" ;first language is the default language
  
LangString app_AppName ${LANG_ENGLISH} "iBrew"
LangString app_WelcomePageTitle ${LANG_ENGLISH} \
		"iBrew Installer"
LangString app_WelcomePageText ${LANG_ENGLISH} \
        "Release: ${RELEASE_STR}$\n$\r$\n$\r\
        This installer will guide you through the process of installing iBrew.$\n$\r $\n$\r"
LangString app_LicensePageTextTop ${LANG_ENGLISH} "iBrew End-user License Agreement"
LangString app_FinishPageTitle ${LANG_ENGLISH} \
		"iBrew Installer"
LangString app_FinishPageText ${LANG_ENGLISH} \
		"Installation complete!"
LangString app_FinishPageLink ${LANG_ENGLISH} "iBrew development site"

LangString LicenseFile ${LANG_ENGLISH} 		 "LICENSE"  ;;these two should be the same
LicenseLangString LicenseRTF ${LANG_ENGLISH} "LICENSE"