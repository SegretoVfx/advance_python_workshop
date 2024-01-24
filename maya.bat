::------------------------------------------------------------
:: --- Maya environment ---
:: Description   = Create the studio tool environment for Maya
:: 
:: Date   = 2024 - 01 - 23
:: Author = Juls
:: Email  = segretovfx@gmail.com
::------------------------------------------------------------
@echo off

::------------------------------------------------------------
:: --- MAYA VERSION ---
set "MAYA_VERSION=2024"
set "MAYA_PATH=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"

:: --- DISABLE REPORTS ---
set "MAYA_DISABLE_CLIC_IPM=1"
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"
set "MAYA_DISABLE_ADP=1"

::------------------------------------------------------------
:: --- PATHS ---
set "STUDIO_TOOLS_ROOT=P:\PYTHON\advance_python_workshop\01_app"
set "STUDIO_TOOLS_NAME=workshop_assignment"
:: --- SUB PATH ---
set "STUDIO_TOOLS_PATH=%STUDIO_TOOLS_ROOT%\%STUDIO_TOOLS_NAME%\dev"

:: --- MODULES ---
set "MODULES_PATH=%STUDIO_TOOLS_PATH%\modules"
set "MLTOOLS_PATH=%STUDIO_TOOLS_PATH%\modules\ml_tools"
set "WSTOOLS_PATH=%STUDIO_TOOLS_PATH%\modules\workshop_tools"
:: --- PLUG-INS ---
set "PLUG_IN_PATH=%STUDIO_TOOLS_PATH%\plug-ins"
:: --- SHELF ---
set "SHELVES_PATH=%STUDIO_TOOLS_PATH%\shelves"
:: --- PACKAGES ---
set "PACKAGE_PATH=%STUDIO_TOOLS_PATH%\packages"
:: --- PYTHON ---
set "PYTHON_PATH=%STUDIO_TOOLS_PATH%\scripts\py"
:: --- MEL SCRIPTS ---
set "MEL_PATH=%STUDIO_TOOLS_PATH%\scripts\mel"
:: --- IMAGES ---
set "ICONS_PATH=%STUDIO_TOOLS_PATH%\img"

::------------------------------------------------------------
:: --- ENVIRONMENT VAR ---
:: --- MODULES ---
set "MAYA_MODULE_PATH=%MODULES_PATH%;%MAYA_MODULE_PATH%"
set "MAYA_MODULE_PATH=%MLTOOLS_PATH%;%MAYA_MODULE_PATH%"
set "MAYA_MODULE_PATH=%WSTOOLS_PATH%;%MAYA_MODULE_PATH%"
:: --- PLUG-INS ---
set "MAYA_PLUG_IN_PATH=%PLUG_IN_PATH%;%MAYA_PLUG_IN_PATH%"
:: --- SHELF ---
set "MAYA_SHELF_PATH=%SHELVES_PATH%;%MAYA_SHELF_PATH%"
:: --- PACKAGES ---
set "MAYA_PACKAGE_PATH=%PACKAGE_PATH%;%MAYA_PACKAGE_PATH%"
:: --- PYTHON ---
set "PYTHONPATH=%PYTHON_PATH%;%PYTHONPATH%"
:: --- MEL SCRIPTS ---
set "MAYA_SCRIPT_PATH=%MEL_PATH%;%MAYA_SCRIPT_PATH%"
:: --- IMAGES ---
set "XBMLANGPATH=%ICONS_PATH%;%XBMLANGPATH%"

:: --- MAYA ---
set "PATH=%MAYA_PATH%\bin;%PATH%"

:: --- CALL MAYA ---
:: Launch Maya inside the current environment.
if "%1"=="" (
  start "" "maya.exe"
) else (
  start "" "maya.exe" -file "%1"
)

exit