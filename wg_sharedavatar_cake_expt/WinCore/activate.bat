@echo off
SET "CONAN_OLD_PATH=%PATH%"

FOR /F "usebackq tokens=1,* delims==" %%i IN ("C:\Users\hapticslab\InUsers\nishimura\wg-sharedavatar-cake-expt\wg_sharedavatar_cake_expt\WinCore\environment.bat.env") DO (
    CALL SET "%%i=%%j"
)

SET "CONAN_OLD_PROMPT=%PROMPT%"
SET "PROMPT=(conanenv) %PROMPT%"