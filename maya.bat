@echo off
:: MAYA

:: --- MAYA VERSION ---
set "MAYA_VERSION=2024"
set "MAYA_PATH=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"

:: --- DISABLE REPORTS ---
set "MAYA_DISABLE_CLIC_IPM=1"
set "MAYA_DISABLE_CIP=1"
set "MAYA_DISABLE_CER=1"
set "MAYA_DISABLE_ADP=1"

:: --- PATHS ---
set "STUDIO_TOOLS_ROOT=P:\PYTHON\advance_python_workshop\01_app"
set "STUDIO_TOOLS_NAME=Juls_toolbox"

set "STUDIO_TOOLS_PATH=%STUDIO_TOOLS_ROOT%\%STUDIO_TOOLS_NAME%\dev"

:: --- VARIABLES ---
:: Variable used locally created for readability.
set "MODULES=%STUDIO_TOOLS_PATH%\modules"
set "ML_TOOLS=%STUDIO_TOOLS_PATH%\modules\ml_tools"
set "JULS_TOOLS=%STUDIO_TOOLS_PATH%\modules\juls_tools"
set "PLUG-INS=%STUDIO_TOOLS_PATH%\plug-ins"
set "SHELVES=%STUDIO_TOOLS_PATH%\shelves"
set "PACKAGES=%STUDIO_TOOLS_PATH%\packages"
set "ICONS=%STUDIO_TOOLS_PATH%\img\juls_tools_icons"
set "PYTHON=%STUDIO_TOOLS_PATH%\scripts\py"
set "MEL=%STUDIO_TOOLS_PATH%\scripts\mel"

::------------------------------------------------------------
:: --- ENVIRONMENT VAR ---

:: --- PYTHON ---
set "PYTHONPATH=%PYTHON%;%PYTHONPATH%"
:: --- MEL SCRIPTS ---
set "MAYA_SCRIPT_PATH=%MEL%;%MAYA_SCRIPT_PATH%"
:: --- ADDING MODULES ---
set "MAYA_MODULE_PATH=%MODULES%;%MAYA_MODULE_PATH%"
set "MAYA_MODULE_PATH=%ML_TOOLS%;%MAYA_MODULE_PATH%"
set "MAYA_MODULE_PATH=%JULS_TOOLS%;%MAYA_MODULE_PATH%"
:: --- PLUG-INS ---
set "MAYA_PLUG_IN_PATH=%PLUG-INS%;%MAYA_PLUG_IN_PATH%"
:: --- SHELF ---
set "MAYA_SHELF_PATH=%SHELVES%;%MAYA_SHELF_PATH%"
:: --- PACKAGES ---
set "MAYA_PACKAGE_PATH=%PACKAGES%;%MAYA_PACKAGE_PATH%"
:: --- IMAGES ---
set "XBMLANGPATH=%ICONS%;%XBMLANGPATH%"


:: --- Arnold ---
set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%
:: --- RENDERING ---
:: --- ARNOLD ---
set "ARNOLD_PATH=%PLUGINS_PATH%/arnold"
set "MtoA=%ARNOLD_PATH%/%MAYA_VERSION%"
set "MAYA_MODULE_PATH=%MtoA%;%MAYA_MODULE_PATH%"
set "PATH=%MtoA%/bin;%PATH%"
set "ARNOLD_PLUGIN_PATH=%MtoA%/shaders;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_PLUGIN_PATH=%ARNOLD_PATH%/bin;%ARNOLD_PLUGIN_PATH%;%ARNOLD_PLUGIN_PATH%"
set "ARNOLD_LICENSE_HOST=blue"

:: --- RENDERMAN ---
set "RM=%PLUGINS_PATH%/renderman/RenderManStudio-20.9-maya%MAYA_VERSION%"
set "MAYA_MODULE_PATH=%RM%/etc;%MAYA_MODULE_PATH%"
set "RMSTREE=%RM%"
set "PATH=%RM%/bin;%PATH%"

:: --- MAYA ---
set "PATH=%MAYA_PATH%\bin;%PATH%"

:: --- CALL MAYA ---
:: Launch Maya inside the current environment.
if "%1"=="" (
  start "" "%MAYA_PATH%\bin\maya.exe"
) else (
  start "" "%MAYA_PATH%\bin\maya.exe" -file "%1"
)

exit