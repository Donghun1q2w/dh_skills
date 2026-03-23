@echo off
cd /d %~dp0
echo === E3D Standalone Test Launcher ===
echo.

REM Set AVEVA E3D path and add to PATH for runtime DLL loading
SET AVEVA_DESIGN_EXE=C:\cae_prog\AVEVA\v2.x\e3d\
SET PATH=C:\cae_prog\AVEVA\v2.x\e3d\;%PATH%

REM Load project environment variables
echo Loading project environment variables...
call "J:\cae_proj\evarProj.bat"
echo Done.
echo.

REM Run
echo Running test...
echo.
bin\x86\Debug\E3DStandaloneTest.exe
echo.
echo Return code: %ERRORLEVEL%
pause
