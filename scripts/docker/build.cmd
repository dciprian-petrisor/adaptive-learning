@echo off

for %%i in ("%~dp1.") do set "folder=%%~fi"
pushd %folder%
set tag="latest"

if [%1] NEQ [] (
set tag=%1
)

echo %cd%
docker build -t adaptive_learning_backend:%tag% .

popd