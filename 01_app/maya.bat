@echo off
:: MAYA

:: --- SET VARIABLES ---

set "PROJECT_NAME=Juls_toolbox"
set "DEV=dev"
set "SCRIPTS=scripts"
set "ICONS=icons"
set "SHELF=shelf"

:: --- PATHS ---

set "PIPE_ROOT=P:\PYTHON\advance_python_workshop\01_app"

set "PROJECT_ROOT=%PIPE_ROOT%\%PROJECT_NAME%"

:: --- MAYA VERSION ---

set "MAYA_VERSION=2024"

:: --- PIPELINE ---
set "PIPELINE_PATH=%PROJECT_ROOT%\%DEV%"

:: --- PYTHON ---
set "PYTHON_PATH=%PROJECT_ROOT%\%SCRIPTS%"

:: --- SHELF ---
set "MAYA_SHELF_PATH=%PIPELINE_PATH%\%SHELF%;%MAYA_SHELF_PATH%"

:: --- SPLASHSCREEN ---
set "XBMLANGPATH=%PIPELINE_PATH%\%ICONS%;%XBMLANGPATH%"



:: --- Arnold ---
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%
set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%


:: --- CALL MAYA ---
set "MAYA_DIR=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%\bin;%PATH%"
start "" "%MAYA_DIR%\bin\maya.exe"
