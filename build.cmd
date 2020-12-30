@echo off

set tag="latest"

if [%1] NEQ [] (
set tag=%1
)

docker build -t adaptive_learning_backend:%tag% .