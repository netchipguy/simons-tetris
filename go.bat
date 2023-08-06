
python -m PyInstaller tetris.py --clean -y -w --onefile ^
--workpath c:\nobackup\tetris\pyinstaller\build ^
--distpath c:\nobackup\tetris\pyinstaller\dist ^
--add-data "tetris.png;." ^
--add-data "tetris.mp3;." ^
--add-data "modern-tetris.ttf;." ^
--add-data "tetris_icon.png;." ^
--add-data "brick_*.png;." ^
--icon tetris_icon.ico

