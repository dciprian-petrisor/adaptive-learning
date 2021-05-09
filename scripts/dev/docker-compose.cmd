@echo off

call "%~dp0.\load-secrethub-credentials.cmd"

for %%i in ("%~dp1.") do set "folder=%%~fi"
pushd %folder%

docker compose up