Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run chr(34) & scriptDir & "\.venv\Scripts\python.exe" & chr(34) & " " & chr(34) & scriptDir & "\app.py" & chr(34), 0, False
