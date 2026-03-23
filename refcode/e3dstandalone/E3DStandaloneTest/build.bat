@echo off
cd /d %~dp0
C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe E3DStandaloneTest.csproj /p:Configuration=Debug /p:Platform=x86 /verbosity:minimal
