@echo off
set MY_PATH=%~dp0
set MY_DIR=%MY_PATH:config\=wg_sharedavatar_cake_expt\WinCore%
FOR /F "usebackq tokens=1,* delims==" %%i IN ("%CD%\config\core_activate_win.bat.env") DO (
    CALL SET "%%i=%%j"
)
