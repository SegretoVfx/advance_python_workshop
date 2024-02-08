::------------------------------------------------------------
:: --- Maya environment ---
:: Description   = Launch Maya in a project environment  
:: 
:: Date   = 2024 - 02 - 07
:: Author = Juls
:: Email  = segretovfx@gmail.com
::------------------------------------------------------------
@echo off

::------------------------------------------------------------
:: --- PATHS ---
set "PROJECT_ROOT=P:\PYTHON\advance_python_workshop\01_app"

:: --- MODULES ---
set "MODULES_PATH=%PROJECT_ROOT%\modules"
set "ML_MODULE=%PROJECT_ROOT%\modules\ml_tools"
:: --- SHELF ---
set "SHELVES_PATH=%PROJECT_ROOT%\shelves"
:: --- PYTHON ---
set "PYTHON_PATH=%PROJECT_ROOT%\scripts"
:: --- IMAGES ---
set "ICONS_PATH=%PROJECT_ROOT%\icons"

:: --- DEFAULT PROJECT FOLDER ---
set "PROJECT_PATH=P:\PYTHON\advance_python_workshop\maya-scene"


::------------------------------------------------------------
:: --- MAYA VERSION ---
set "MAYA_VERSION=2024"
set "MAYA_PATH=C:\Program Files\Autodesk\Maya%MAYA_VERSION%\bin"

:: --- DISABLE REPORTS ---
set "MAYA_DISABLE_CLIC_IPM=1"
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"
set "MAYA_DISABLE_ADP=1"

::------------------------------------------------------------
:: --- ENVIRONMENT VAR ---
:: --- MODULES ---
set "MAYA_MODULE_PATH=%MODULES_PATH%;%MAYA_MODULE_PATH%"
set "MAYA_MODULE_PATH=%ML_MODULE%;%MAYA_MODULE_PATH%"
:: --- SHELF ---
set "MAYA_SHELF_PATH=%SHELVES_PATH%;%MAYA_SHELF_PATH%"
:: --- PYTHON ---
set "PYTHONPATH=%PYTHON_PATH%;%PYTHONPATH%"
:: --- IMAGES ---
set "XBMLANGPATH=%ICONS_PATH%;%XBMLANGPATH%"
:: --- MAYA PROJECT ---
::set "MAYA_PROJECTS_DIR=%PROJECT_PATH%"
set "MAYA_PROJECT=%PROJECT_PATH%"

:: --- MAYA PATH ---
set "PATH=%MAYA_PATH%;%PATH%"


:: --- CALL MAYA ---
:: Launch Maya inside the current environment.
if "%1"=="" (
  start "" "maya.exe"
) else (
  start "" "maya.exe" -file "%1"
)

exit