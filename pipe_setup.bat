@echo off
:: MAYA

:: --- VARIABLES ---
:: Variable used locally created for readability.
set "dev=dev"
set "modules=modules"
set "plugins=plugins"
set "shelf=shelf"
set "packages=packages"
set "icons=icons"
set "scripts=scripts"
set "py=py"
set "mel=mel"
:: Path for the current project.
set "MASTER_ROOT=P:\PYTHON\advance_python_workshop\01_app"
set "PROJECT_NAME=workshop_assignment"

:: --- PATHS ---
:: Variables setting up the paths to the tree hierarchy.
set "PROJECT_ROOT=%MASTER_ROOT%\%PROJECT_NAME%"
set "PIPELINEPATH=%PROJECT_ROOT%\%dev%"
if not exist %PIPELINEPATH% md %PIPELINEPATH%

:: --- ENVIRONMENT VAR ---
:: Adding the project's path to the environment variables.
:: --- PYTHON ---
set "script_py=%PIPELINEPATH%\%scripts%\%py%"
if not exist %script_py% md %script_py%

:: --- MEL SCRIPTS ---
set "script_mel=%PIPELINEPATH%\%scripts%\%mel%"
if not exist %script_mel% md %script_mel%

:: --- MODULES ---
set "modules=%PIPELINEPATH%\%modules%"
if not exist %modules% md %modules%

:: --- PLUGINS ---
set "plugins=%PIPELINEPATH%\%plugins%"
if not exist %plugins% md %plugins%

:: --- SHELF ---
set "shelf=%PIPELINEPATH%\%shelf%"
if not exist %shelf% md %shelf%

:: --- PACKAGES ---
set "package=%PIPELINEPATH%\%packages%"
if not exist %package% md %package%

:: --- SPLASHSCREEN ---
set "icons=%PIPELINEPATH%\%icons%"
if not exist %icons% md %icons%


exit
