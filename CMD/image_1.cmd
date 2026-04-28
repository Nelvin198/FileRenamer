@echo off
setlocal EnableExtensions EnableDelayedExpansion

set /p PARTIAL=Text to match in filename: 
set /p NEWNAME=New base name: 

set n=1

for %%f in (*.*) do (
    echo %%~nf | find /I "%PARTIAL%" >nul
    if not errorlevel 1 (
        ren "%%f" "%NEWNAME%_!n!%%~xf"
        set /a n+=1
    )
)

echo Done.
pause