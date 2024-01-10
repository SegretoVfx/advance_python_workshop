@echo off
:: MAYA

:: --- PATHS ---
:: Path for the current project.
set "MASTER_ROOT=P:\PYTHON\advance_python_workshop\01_app"
set "PROJECT_NAME=Juls_toolbox"
:: Variables setting up the paths to the tree hierarchy.
set "PROJECT_ROOT=%MASTER_ROOT%\%PROJECT_NAME%"
set "PIPELINEPATH=%PROJECT_ROOT%\dev"

:: --- VARIABLES ---
:: Variable used locally created for readability.
set "modules=%PIPELINEPATH%\modules"
set "ml_tools=%PIPELINEPATH%\modules\ml_tools"
set "plug-ins=%PIPELINEPATH%\plug-ins"
set "shelves=%PIPELINEPATH%\shelves"
set "packages=%PIPELINEPATH%\packages"
set "icons=%PIPELINEPATH%\icons"
set "python=%PIPELINEPATH%\scripts\py"
set "mel=%PIPELINEPATH%\scripts\mel"

:: --- ENVIRONMENT VAR ---
:: Adding the project's path to the environment variables.
:: --- PYTHON ---
set "PYTHONPATH=%python%"

:: --- MEL SCRIPTS ---
set "MAYA_SCRIPT_PATH=%mel%"

:: --- MODULES ---
set "MAYA_MODULE_PATH=%modules%;%ml_tools%;%MAYA_MODULE_PATH%"

:: --- PLUG-INS ---
set "MAYA_PLUG_IN_PATH=%plug-ins%;%MAYA_PLUG_IN_PATH%"

:: --- SHELF ---
set "MAYA_SHELF_PATH=%shelves%;%MAYA_SHELF_PATH%"

:: --- PACKAGES ---
set "MAYA_PACKAGE_PATH=%packages%;%MAYA_PACKAGE_PATH%"

:: --- SPLASHSCREEN ---
set "XBMLANGPATH=%icons%;%XBMLANGPATH%"


:: --- MAYA VERSION ---
set "MAYA_VERSION=2024"

:: --- Arnold ---
set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%


:: --- CALL MAYA ---
:: Launch Maya inside the current environment.
set "MAYA_DIR=C:\Program Files\Autodesk\Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%\bin;%PATH%"
start "" "%MAYA_DIR%\bin\maya.exe"
