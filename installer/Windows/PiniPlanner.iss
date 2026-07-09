#define MyAppName "PiniPlanner"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "José"
#define MyAppExeName "PiniPlanner.exe"

[Setup]
AppId={{8F01B4E7-0F4D-4B0B-8C3E-PINIPLANNER01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\output
OutputBaseFilename=PiniPlanner_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Files]
Source: "..\..\dist\PiniPlanner\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PiniPlanner"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\PiniPlanner"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir PiniPlanner"; Flags: nowait postinstall skipifsilent