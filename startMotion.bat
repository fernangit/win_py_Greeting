rem move browser to front
E:\work\win_py_Greeting\activate.vbs msedge.exe
rem wait 3sec
timeout /t 3 > nul
rem call motion
E:\work\win_py_Greeting\venv\Scripts\python motion.py %1
