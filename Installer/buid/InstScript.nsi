!define PRODUCT_NAME "Auto Movie Archive" 
!define PRODUCT_VERSION "0.1" 
!define PRODUCT_PUBLISHER "TJ Young" 
!define PRODUCT_WEB_SITE "http://brendonbeebe.github.com/AutoMovieArchive/"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE_RADIOBUTTONS
!insertmacro MUI_PAGE_LICENSE "License.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "setup.exe"
InstallDir "$PROGRAMFILES\AMA"


Section ""
	SetOutPath "$INSTDIR"
	SetOverwrite ifnewer
	File /r "pkgs"
	ReadRegStr $0 HKLM "SOFTWARE\VideoLAN\VLC" "Version"
	${if} $0 == "2.0.5"
		goto endvlc
	${EndIf}
	ExecWait '"$INSTDIR\pkgs\vlc.exe"'
	endvlc:
SectionEnd