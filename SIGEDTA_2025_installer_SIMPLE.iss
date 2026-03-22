; ========= Inno Setup script for SIGEDTA_2025 (VERSION SIMPLE SIN IMAGENES) =========
#define AppName "SIGEDTA"
#define AppVersion "2.0"
#define AppPublisher "Fiscalía Especial de Medio Ambiente (FEMA)"
#define ExeName "SIGEDTA.exe"

[Setup]
AppId={{9A9F5F2C-9B8E-46EE-9C5F-86B5B6E2A2B1}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableDirPage=no
DisableProgramGroupPage=yes
LicenseFile=license.txt
OutputBaseFilename=Setup_SIGEDTA_2025
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
SetupIconFile=assets\icon_sigedta.ico
; Comentadas las imágenes problemáticas del wizard
; WizardImageFile=assets\logo_sigedta.bmp
; WizardSmallImageFile=assets\icon_sigedta.ico

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Files]
Source: "dist\SIGEDTA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon_sigedta.ico"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#ExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon_sigedta.ico"

[Run]
Filename: "{app}\{#ExeName}"; Description: "Iniciar {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data\backups"
