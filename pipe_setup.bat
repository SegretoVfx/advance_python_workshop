:: --- BUILD PIPELINE STRUCTURE ---
@echo off
:: PIPELINE

:: --- PATHS ---
set "PIPELINE_ROOT=P:\PYTHON\advance_python_workshop\01_app"
set "PIPELINE_NAME=workshop_assignment"

set "PIPELINE_PATH=%PIPELINE_ROOT%\%PIPELINE_NAME%\dev"
if not exist %PIPELINE_PATH% md %PIPELINE_PATH%

:: --- VARIABLES ---
:: CREATE folder tree inside the PIPELINE_NAME root folder if not exists.
set "MODULES=%PIPELINE_PATH%\modules"
if not exist %MODULES% md %MODULES%

set "PLUG-INS=%PIPELINE_PATH%\plug-ins"
if not exist %PLUG-INS% md %PLUG-INS%

set "SHELVES=%PIPELINE_PATH%\shelves"
if not exist %SHELVES% md %SHELVES%

set "PACKAGES=%PIPELINE_PATH%\packages"
if not exist %PACKAGES% md %PACKAGES%

set "IMG=%PIPELINE_PATH%\img"
if not exist %IMG% md %IMG%

set "PYTHON=%PIPELINE_PATH%\scripts\py"
if not exist %PYTHON% md %PYTHON%
set "MEL=%PIPELINE_PATH%\scripts\mel"
if not exist %MEL% md %MEL%

exit
