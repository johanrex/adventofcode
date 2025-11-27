@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
cl.exe /std:c++20 /Zc:__cplusplus /Zi /Od /W4 /EHsc "%~1" /Fe:"%~dpn1.exe"