CD %~dp0
call .venv\Scripts\activate.bat
call .\config\core_activate_win.bat
python .\wg_sharedavatar_cake_expt\collaborative_app.py
