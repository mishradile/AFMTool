Set oShell = CreateObject("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c main.bat"
oShell.Run strArgs,0,false