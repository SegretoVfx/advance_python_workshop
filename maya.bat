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
set "PROJECT_NAME=Juls_toolbox"

:: --- PATHS ---
:: Variables setting up the paths to the tree hierarchy.
set "PROJECT_ROOT=%MASTER_ROOT%\%PROJECT_NAME%"
set "PIPELINEPATH=%PROJECT_ROOT%\%dev%"

:: --- ENVIRONMENT VAR ---
:: Adding the project's path to the environment variables.
:: --- PYTHON ---
set "PYTHONPATH=%PIPELINEPATH%\%scripts%\%py%"

:: --- MEL SCRIPTS ---
set "MAYA_SCRIPT_PATH=%PIPELINEPATH%\%scripts%\%mel%"

:: --- MODULES ---
set "MAYA_MODULE_PATH=%PIPELINEPATH%\%modules%;%MAYA_MODULE_PATH%"

:: --- PLUGINS ---
set "MAYA_PLUG_IN_PATH=%PIPELINEPATH%\%plugins%;%MAYA_PLUG_IN_PATH%"

:: --- SHELF ---
set "MAYA_SHELF_PATH=%PIPELINEPATH%\%shelf%;%MAYA_SHELF_PATH%"

:: --- PACKAGES ---
set "MAYA_PACKAGE_PATH=%PIPELINEPATH%\%packages%;%MAYA_PACKAGE_PATH%"

:: --- SPLASHSCREEN ---
set "XBMLANGPATH=%PIPELINEPATH%\%icons%;%XBMLANGPATH%"


:: --- MAYA VERSION ---
set "MAYA_VERSION=2024"

:: --- Arnold ---
set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%


:: --- CALL MAYA ---
:: Launch Maya inside the current environment.
set "MAYA_DIR=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%\bin;%PATH%"
start "" "%MAYA_DIR%\bin\maya.exe"
