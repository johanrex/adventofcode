@echo off
REM Skip env setup if already in a VS dev environment
if defined VSCMD_VER goto build
if defined VCINSTALLDIR goto build

call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"

:build
cl.exe /std:c++latest /Zc:__cplusplus /Zi /Od /W4 /EHsc "%~1" /Fe:"%~dpn1.exe"