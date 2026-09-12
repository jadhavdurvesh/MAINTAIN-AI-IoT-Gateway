#define MyAppName "MAINTAIN AI IoT Gateway"
#define MyAppPublisher "MAINTAIN AI"
#define MyAppExeName "MAINTAIN AI IoT Gateway.exe"
#ifndef MyAppVersion
  #define MyAppVersion "0.1.0"
#endif

[Setup]
AppId={{8B0D6C8A-4B2A-4C9B-9B8D-2E0D0A8A5F21}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\MAINTAIN AI\IoT Gateway
DefaultGroupName=MAINTAIN AI
OutputDir=installer-output
OutputBaseFilename=MAINTAIN-AI-IoT-Gateway-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\dist\MAINTAIN AI IoT Gateway.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MAINTAIN AI IoT Gateway"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\MAINTAIN AI IoT Gateway"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch MAINTAIN AI IoT Gateway"; Flags: nowait postinstall skipifsilent
