; ========= Inno Setup script for SISTECDATOSFEMA =========
#define AppName "SISTECDATOSFEMA"
#define AppVersion "3.0"
#define AppPublisher "Fiscalía Especial de Medio Ambiente (FEMA) y Fernando R. Ardón"
#define ExeName "SISTECDATOSFEMA.exe"

[Setup]
AppId={{9A9F5F2C-1234-5678-9C5F-86B5B6E2A2B1}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableDirPage=no
DisableProgramGroupPage=yes
OutputBaseFilename=Setup_SISTECDATOSFEMA_v3
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
SetupIconFile=assets\icon_sistecdatos.ico

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Files]
Source: "dist\SISTECDATOSFEMA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon_sistecdatos.ico"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#ExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon_sistecdatos.ico"

[Run]
Filename: "{app}\{#ExeName}"; Description: "Iniciar {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data\backups"
