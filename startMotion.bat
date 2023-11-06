rem move browser to front
.\activate.vbs msedge.exe
rem wait 3sec
timeout /t 3 > nul
rem call motion
python motion.py %1
