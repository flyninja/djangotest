@echo off

echo [*]INFO: clean previos

if exist build del build || goto error

echo [*]INFO: prepare output

if not exist build mkdir build || goto error

echo [*]INFO: build django project

python src\build.py || goto error


echo [*]INFO: build success

goto ret

:error

echo [-]ERROR: _

:ret

pause