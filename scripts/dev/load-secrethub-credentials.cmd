@echo off

if not exist %HOME% (
    echo "HOME variable is not defined. Please define it and try again."
)

if not exist %HOME%\.secrethub\credential (
    echo "Failed to find credential file in %HOME%\.secrethub\credential"
)

for /F %%A in ('type %HOME%\.secrethub\credential') do set "SECRETHUB_CREDENTIAL=%%~A"
